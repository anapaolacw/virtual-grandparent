from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
   path('', views.chats, name='chats'),
   path('<slug:slug>/', views.chat, name='chat'),
]