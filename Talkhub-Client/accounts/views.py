from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Exists, OuterRef
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest
from urllib.parse import urlparse
from django.template.loader import render_to_string
import requests, random, json,socketio
sio = socketio.Client()
from .forms import SignupForm, LoginForm
from .models import User, Online, History

sio=socketio.Client()
# -------------------------------
# Utility: Generate Unique 10-digit UserID
# -------------------------------
def generate_unique_userid():
    while True:
        uid = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        if not User.objects.filter(userid=uid).exists():
            return uid

# -------------------------------
# Signup View
# -------------------------------
def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            userid = form.cleaned_data['userid']
            if not userid:
                userid = generate_unique_userid()
            elif User.objects.filter(userid=userid).exists():
                form.add_error('userid', 'UserID already exists')
                return render(request, 'accounts/signup.html', {'form': form})
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'accounts/signup.html', {'form': form})

# -------------------------------
# Login View
# -------------------------------
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            userid = form.cleaned_data['userid']
            password = form.cleaned_data['password']
            user = authenticate(request, userid=userid, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Welcome back!")
                return redirect(request.GET.get('next') or 'dashboard')
            else:
                form.add_error(None, 'Invalid UserID or Password')
    else:
        form = LoginForm()
        if 'next' in request.GET:
            messages.warning(request, "You must log in to view that page.")
    return render(request, 'accounts/login.html', {'form': form})

# -------------------------------
# Dashboard
# -------------------------------
@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

# -------------------------------
# Start Chatting → Get Relay ID and Go to Chat
# -------------------------------
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
import requests

from .models import Online

@login_required
def start_chatting(request):
    user = request.user

    # If already online, skip
    if Online.objects.filter(user=user).exists():
        return redirect('chat')

    try:
        # ✅ Correct endpoint to request new relay ID
        response = requests.get(settings.RELAY_SERVER_URL + "new-id", timeout=5)
        if response.status_code == 200:
            relay_id = str(response.json().get('relay_id', ''))
            if not relay_id.isdigit() or len(relay_id) != 4:
                raise ValueError("Invalid relay ID format")
        else:
            raise Exception("Failed to fetch relay ID")
    except Exception as e:
        print("⚠️ Relay server error:", e)
        relay_id = "-1"

    # If relay server failed, show server busy page
    if relay_id == "-1":
        return render(request, "accounts/server_busy.html", status=503)

    # Save relay ID to Online table
    Online.objects.filter(user=user).delete()
    Online.objects.create(user=user, relay_id=relay_id)

    return redirect('chat')

# -------------------------------
# Chat View
# -------------------------------
@login_required
def chat_view(request, user_id=None):
    # ✅ Show only users with whom current user has chat history
    users = User.objects.annotate(
        has_history=Exists(
            History.objects.filter(
                Q(sender=request.user, receiver=OuterRef('pk')) |
                Q(sender=OuterRef('pk'), receiver=request.user)
            )
        )
    ).filter(has_history=True).exclude(id=request.user.id)

    # ✅ Who is online (for green dot)
    online_ids = Online.objects.values_list('user_id', flat=True)

    active_user = None
    chat_history = []

    # ✅ Handle 10-digit ID add
    if request.method == 'POST' and 'add_user' in request.POST:
        new_userid = request.POST.get('new_userid')
        if new_userid and len(new_userid) == 10 and new_userid.isdigit():
            try:
                user = User.objects.get(userid=new_userid)
                return redirect('chat_with_user', user_id=user.id)
            except User.DoesNotExist:
                messages.error(request, "User with that ID not found.")
        else:
            messages.error(request, "Enter a valid 10-digit UserID.")

    # ✅ Load chat history if user selected
    if user_id:
        active_user = get_object_or_404(User, id=user_id)
        chat_history = History.objects.filter(
            Q(sender=request.user, receiver=active_user) |
            Q(sender=active_user, receiver=request.user)
        ).order_by('timestamp')

    # ✅ Relay info for JS to use
    relay_url = settings.RELAY_SERVER_URL
    relay_server_ip = urlparse(relay_url).hostname or "127.0.0.1"

    receiver_relay_id = ""
    if active_user:
        entry = Online.objects.filter(user=active_user).first()
        if entry:
            receiver_relay_id = entry.relay_id

    return render(request, 'accounts/chat.html', {
        'users': users,
        'online_ids': online_ids,
        'active_user': active_user,
        'chat_history': chat_history,
        'relay_server_ip': relay_server_ip,
        'receiver_relay_id': receiver_relay_id,
    })

# -------------------------------
# Send a Message (Server handles relay + DB)
# -------------------------------
@login_required
def send_message_view(request, user_id):
    if request.method == "POST":
        receiver = get_object_or_404(User, id=user_id)
        message = request.POST.get("message", "").strip()

        if message:
            # 1. Save to DB
            History.objects.create(sender=request.user, receiver=receiver, message=message)

            # 2. Try sending to relay if both users are online
            try:
                receiver_entry = Online.objects.filter(user=receiver).first()
                sender_entry = Online.objects.filter(user=request.user).first()

                if receiver_entry and sender_entry:
                    relay_payload = {
                        "to": receiver_entry.relay_id,
                        "message": f"{sender_entry.user.name}: {message}"
                    }

                    # Connect to relay and emit once
                    relay_url = settings.RELAY_SERVER_URL.replace("https://", "http://")
                    sio.connect(relay_url)
                    sio.emit("private_message", relay_payload)
                    sio.disconnect()

            except Exception as e:
                print("Relay send failed:", e)

        return redirect('chat_with_user', user_id=user_id)
    return HttpResponseBadRequest("Invalid method")

# -------------------------------
# Save message from relay (incoming)
# -------------------------------
@csrf_exempt
@login_required
def save_from_relay(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            relay_id = str(data.get("relay_id", "")).strip()
            message = data.get("message", "").strip()

            if not relay_id or not message:
                return HttpResponseBadRequest("Missing relay_id or message")

            try:
                sender_entry = Online.objects.get(relay_id=relay_id)
                sender = sender_entry.user
                receiver = request.user

                History.objects.create(
                    sender=sender,
                    receiver=receiver,
                    message=message
                )
                return HttpResponse("OK")
            except Online.DoesNotExist:
                return HttpResponseBadRequest("Invalid relay ID")

        except Exception as e:
            return HttpResponseBadRequest(f"Error: {str(e)}")
    return HttpResponseBadRequest("Invalid method")

# -------------------------------
# Logout → Remove Online Status
# -------------------------------
@login_required
def logout_view(request):
    Online.objects.filter(user=request.user).delete()
    logout(request)
    return redirect('login')

@login_required
def fetch_messages(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    chat_history = History.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')

    html = render_to_string('accounts/partials/messages.html', {
        'chat_history': chat_history,
        'request': request,
    })
    return HttpResponse(html)

@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')

        if name:
            user.name = name
        if password:
            user.set_password(password)
        user.save()
        messages.success(request, "Profile updated.")
        return redirect('profile')

    return render(request, 'accounts/profile.html', {'user': user})
