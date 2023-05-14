# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from marketplace import settings
import asyncio
from asgiref.sync import async_to_sync, sync_to_async

from .models import Message
from django.contrib.auth.models import User

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        self.lastmsgs = async_to_sync(Message.lastmsgs)(self.room_name)
        
        for msg in reversed(self.lastmsgs):
            self.send(text_data=json.dumps({
            "username": msg.author.username,
            "message": msg.content,
            }))
        # print(self.lastmsgs)

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        room_name = text_data_json['room_name']
        user_id = text_data_json['user_id']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat.message",
                # "room_id": room_group_name,
                "username": self.scope["user"].username,
                "message": message
            }
        )
        print(user_id)
        current_user = User.objects.get(id=user_id)
        print(current_user)
        b = Message(author=current_user, content=message, room=room_name)
        b.save()

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # # Send message to WebSocket
        self.send(text_data=json.dumps({
            # "msg_type": settings.MSG_TYPE_MESSAGE,
            # "room": event["room_id"],
            "username": event["username"],
            "message": event["message"],
        }))
