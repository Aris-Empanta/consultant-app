import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Profile

# This consumer's sole purpose is to send a notification to 
# a lawyer when an appointment of his is booked by a client.
# So, since it is one-directional, we just have to write only 
# the connect method.
class AppointmentsConsumer(WebsocketConsumer):
    groups = ["appointment_booking"]
    def connect(self):
        # Check if there is an authenticated user and if this user 
        # is a client, else, close the connection.
        # If the connection is valid, we emit a message to the 
        # lawyer in the event payload. The lawyers client websocket handles the rest.
        user = self.scope['user']
        if user.is_authenticated:
            self.accept()
            profile = Profile.objects.filter(user=user).first()
            if profile.Lawyer:
                channel = f'lawyer_{user.username}'
                self.channel_name = channel
                self.send('welcome bro')
            async_to_sync(self.channel_layer.group_add)("appointment_booking", self.channel_name)
            welcome_message = {"message": "Welcome to the WebSocket! You are now connected."}
            self.send(json.dumps(welcome_message))
        else:
            self.close()