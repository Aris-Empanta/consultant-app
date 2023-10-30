import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Profile

# This consumer's sole purpose is to send a notification to 
# a lawyer when an appointment of his is booked by a client.
# So, since it is one-directional, we just have to write only 
# the connect method.
class AppointmentsConsumer(AsyncWebsocketConsumer):

    def connect(self):
        pass
        
    def disconnect(self, code):
        pass
    
    def receive(self, text_data):
        pass