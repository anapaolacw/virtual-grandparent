from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
   # path('', views.chats, name='chats'),
   path('contacts/', views.contacts, name='contacts'),
   path('<int:contact_id>/', views.chat, name='chat'),
   path('getMessages/<int:id>/', views.getMessages, name='getMessages'),
   path('send/', views.send, name='send'),
]