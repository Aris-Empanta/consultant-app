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