from django.shortcuts import redirect
from django.urls import reverse
from accounts.models import Online

class RemoveFromOnlineMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            path = request.path

            allowed_prefixes = [
                reverse('chat'),  # /chat/
                reverse('dashboard'),
                reverse('start_chatting'),reverse('profile'),
            ]

            # Check if current path starts with any allowed prefix
            if not any(path.startswith(prefix) for prefix in allowed_prefixes):
                Online.objects.filter(user=request.user).delete()

        return response
