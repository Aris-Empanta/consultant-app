import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import User, Profile, Messages
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from channels.layers import get_channel_layer

# The consumer for the appointment notifications
class AppointmentsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']

        if not isinstance(user, AnonymousUser):
            profile = await self.get_profile(user)
            if profile.isLawyer:
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

        # We send to the WebSocket client the client's info
        await self.send(text_data=json.dumps({"client": client}))


# The consumer for the messaging between users
class PrivateMessagingConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']

        # We add the connected user in a group that contains his/her username
        if not isinstance(user, AnonymousUser):
            self.group_name = f"user_{user.username}"

            await self.channel_layer.group_add(self.group_name, self.channel_name)
            print(f'{self.channel_name} registered')

        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        receiver = text_data_json['receiver']
        message = text_data_json['message'] 
        
        sender_object = self.scope['user']

        if isinstance(sender_object, AnonymousUser):
            sender = text_data_json['sender']
            sender_object = User.objects.filter(username=sender).first()

        sender = sender_object.username
        avatar = sender_object.profile.avatar.url
        time_sent = timezone.now()
        formatted_time_sent = time_sent.strftime('%d/%m/%Y %H:%M')

        #We save the message to the database.
        await self.save_message(sender_object, receiver, message)

        # First we send the message back to the sender
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'avatar': avatar,
            'time_sent': formatted_time_sent,
            'receiver': receiver,
        }))

        # Then we send message to the receiver if he/she is different
        # than ourselves
        await self.channel_layer.group_send(
            f'user_{receiver}', {
                                "type": "private.message", 
                                'message': message,
                                'sender': sender,
                                'receiver': receiver,
                                'avatar': avatar,
                                'time_sent': formatted_time_sent
                                })

    async def private_message(self, event):

        data = {
                'message' : event['message'],
                'sender' : event['sender'],
                'receiver': event['receiver'],
                'avatar' : event['avatar'],
                'time_sent' : event['time_sent'],
               }

        # We send to the WebSocket both client and lawyer information
        await self.send(text_data=json.dumps(data))

    @database_sync_to_async
    def save_message(self, sender_object, receiver, message):
        message = Messages(sender=sender_object, 
                           receiver=receiver, 
                           message=message)
        message.save()