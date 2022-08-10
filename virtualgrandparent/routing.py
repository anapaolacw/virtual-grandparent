from django import urls
from django.urls import path

from . import consumers

websocket_urlpatterns=[
    urls(r'^ws/(?P<chat_slug>[^/]+)/$', consumers.ChatConsumer.as_asgi()),
]