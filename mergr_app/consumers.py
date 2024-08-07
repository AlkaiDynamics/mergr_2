## consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Message
from .serializers import MessageSerializer
from datetime import datetime

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    """Consumer for handling WebSocket connections for real-time chat."""

    async def connect(self):
        """Handle a new WebSocket connection."""
        self.user = self.scope["user"]
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Handle receiving a message over WebSocket."""
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        receiver_username = text_data_json['receiver']

        # Save message to database
        receiver = await self.get_user_by_username(receiver_username)
        if receiver:
            message_instance = await self.create_message(self.user, receiver, message)
            message_data = MessageSerializer(message_instance).data

            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message_data
                }
            )

    async def chat_message(self, event):
        """Handle sending a message to WebSocket."""
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def get_user_by_username(self, username: str) -> User:
        """Retrieve a User instance by username."""
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    @database_sync_to_async
    def create_message(self, sender: User, receiver: User, content: str) -> Message:
        """Create a new Message instance."""
        return Message.objects.create(
            sender=sender,
            receiver=receiver,
            content=content,
            timestamp=datetime.now()
        )
