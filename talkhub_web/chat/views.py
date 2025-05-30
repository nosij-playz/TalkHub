from django.shortcuts import render
def connect_view(request):
    return render(request, 'connect.html')

def chat_view(request):
    return render(request, 'chat.html')
