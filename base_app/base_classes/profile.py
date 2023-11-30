import uuid
import time
from urllib.parse import unquote 
import asyncio
from websockets import connect
import json 

class BaseProfile:

    PROFILE_PICTURE_MIME_TYPES = [
        'image/jpeg',
        'image/png',
        'image/webp',
        'image/avif',
        'image/tiff',
    ]

    default_profile_pic_name = 'images/profile-pics/avatar.png'

     # The flag to query if the profile's avatar is an 
     # external link or not.
    def is_avatar_external_link(self, image_link):
        is_external = False

        if image_link.startswith('http'):
            is_external = True
            
        return is_external
    
    # The method to add in avatar's name the /media/ in front  
    # if it is from our server's files.
    def format_avatar_link(self, request, avatar_link):
        if avatar_link.startswith('/media/'):
                    avatar_link = avatar_link.replace('/media/', '')

        if(not avatar_link.startswith('http')):
                protocol = "http"

                if request.is_secure():
                    protocol = 'https'                 

                avatar_link = f'{ protocol }://{request.META["HTTP_HOST"]}/media/{avatar_link}'
                return avatar_link
        
        return unquote(avatar_link)
    
    # The method to rename a profile pic image so that it has a
    #  unique name in the server
    def rename_image(self, image_name):
        # We add the timestamp infront so that the image never starts with 
        # http or http like google account images. then we add a unique id, 
        # so that the name is unique, and at the end its extension.
        random_uuid = str(uuid.uuid4())
        timestamp = int(time.time())
        file_extension = image_name.split('.')[-1]
        
        return f'{timestamp}_{random_uuid}.{file_extension}'
    
    def cancel_appointment(self, appointment):
        # On appointment cancellation we modify the following variables as: 
        # client = None, booked = False, checked = False, 
        # time_booked = None, # informed_client = False. 
        # Then send a message to the client.
        appointment.client = None
        appointment.booked = False
        appointment.checked = False
        appointment.time_booked = None
        appointment.informed_client = False

        appointment.save() 
    
    def inform_about_cancellation(self, request, receiver, sender):

        ws_relative_url = "/ws/private-messaging/"
        current_scheme = "wss" if request.is_secure() else "ws"
        websocket_url = f"{current_scheme}://{request.get_host()}{ws_relative_url}"
        message = 'Due to an unexpected occurance, we will have to cancel our appointment. I apologize and look forward to future collaboration.'

        asyncio.run(self.handle_appointment_cancellation_message(websocket_url, receiver, message, sender))
    
    # The method to inform the other party about the appointment cancellation
    async def handle_appointment_cancellation_message(self, websocket_url, receiver, message, sender):
            async with connect(websocket_url) as websocket:
                data = {
                    'receiver': receiver,
                    'message': message,
                    'sender': sender.profile.user.username
                }
                await websocket.send(json.dumps(data))