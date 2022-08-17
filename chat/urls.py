from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
   # path('', views.chats, name='chats'),
   path('contacts/', views.contacts, name='contacts'),
   path('<int:contact_id>/', views.chat, name='chat'),
   path('messages/<int:id>/', views.getMessages, name='getMessages'),
   path('message/send/', views.send, name='send'),
]