import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_slug = self.scope['url_route']['kwargs']['chat_slug']
        self.chat_group_name = 'chat_%s' % self.chat_slug

        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name,
        )