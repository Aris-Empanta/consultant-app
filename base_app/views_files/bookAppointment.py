import json
import asyncio
from websockets import connect
from django.http import JsonResponse
from django.views import View

class BookAppointment(View):
    def post(self, request):
        body = json.loads(request.body)
        client = request.user.username
        lawyer = body['lawyer']

        ws_relative_url = "/ws/book-appointment/"
        current_scheme = "wss" if request.is_secure() else "ws"
        websocket_url = f"{current_scheme}://{request.get_host()}{ws_relative_url}"

        async def send_websocket_data():
            async with connect(websocket_url) as websocket:
                data = {
                    'client': client,
                    'lawyer': lawyer,
                }
                await websocket.send(json.dumps(data))

        asyncio.run(send_websocket_data())

        return JsonResponse({'data': 'received'})