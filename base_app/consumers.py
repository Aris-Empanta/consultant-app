import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class AppointmentsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        client_id = self.scope['user'].id
        lawyer_id = self.scope['url_route']['kwargs']['id']