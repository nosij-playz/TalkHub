from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('start-chatting/', views.start_chatting, name='start_chatting'),
    path('chat/', views.chat_view, name='chat'),
    path('chat/<int:user_id>/', views.chat_view, name='chat_with_user'),
    path('chat/send/<int:user_id>/', views.send_message_view, name='send_message'),
    path('chat/save-from-relay/', views.save_from_relay, name='save_from_relay'),
    path('chat/messages/<int:user_id>/', views.fetch_messages, name='fetch_messages'),
    path('profile/', views.profile_view, name='profile'),
]
