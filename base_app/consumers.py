import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Profile
from channels.db import database_sync_to_async


class AppointmentsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']
       
        profile = await self.get_profile(user)
        print(profile)
        self.accept()
        
    async def disconnect(self, code):
        pass
    
    async def receive(self, text_data):
        pass

    @database_sync_to_async
    def get_profile(self, user):
        return Profile.objects.filter(user=user)[0]