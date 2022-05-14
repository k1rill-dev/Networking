from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('chat/', chat_view, name='chats'),
    path('chat/<int:sender>/<int:receiver>/', message_view, name='chat'),
    path('api/messages/<int:sender>/<int:receiver>/', message_list, name='message-detail'),
    path('api/messages/', message_list, name='message-list'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_view, name='register'),
    path('user/', user, name='user'),
    path('room/', room, name='room'),
    path('selectRoom/', selectRoom, name='selectRoom')
]
