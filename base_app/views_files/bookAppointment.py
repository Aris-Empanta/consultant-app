from django.views import View
from django.http import JsonResponse
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import asyncio
from websockets.sync.client import connect

class BookAppointment(View):
    def post(self, request):
        body = json.loads(request.body)
        client = request.user
        lawyer_username = body['lawyer']

        ws_relative_url = "/ws/book-appointment/"
        current_scheme = "wss" if request.is_secure() else "ws"
        websocket_url = f"{current_scheme}://{request.get_host()}{ws_relative_url}"
        print(websocket_url)

        with connect(websocket_url) as websocket:
            websocket.send("Hello world!")
            message = websocket.recv()
            print(f"Received: {message}")

    

        return JsonResponse({'data': 'received'})