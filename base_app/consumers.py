import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Profile
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser


class AppointmentsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']

        if not isinstance(user, AnonymousUser):
            profile = await self.get_profile(user)
            if profile.Lawyer:
                self.group_name = f"lawyer_{user.username}"
                await self.channel_layer.group_add(self.group_name, self.channel_name)

        await self.accept()
        
    async def disconnect(self, code):
        pass
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        client = text_data_json['client']
        lawyer = text_data_json['lawyer']

        # Send message to room group
        await self.channel_layer.group_send(
            f'lawyer_{lawyer}', {
                                 "type": "appointment.notification", 
                                 "client": client
                                 })

    @database_sync_to_async
    def get_profile(self, user):
        return Profile.objects.filter(user=user).first()
    
    # The handler for appointment notification
    async def appointment_notification(self, event):
        client = event["client"]       

        # We send to the WebSocket both client and lawyer information
        await self.send(text_data=json.dumps({"client": client}))