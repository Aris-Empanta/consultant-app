from django.views import View
from django.http import JsonResponse
import json
from websockets.sync.client import connect

class BookAppointment(View):
    def post(self, request):
        body = json.loads(request.body)
        client = request.user.username
        lawyer = body['lawyer']

        ws_relative_url = "/ws/book-appointment/"
        current_scheme = "wss" if request.is_secure() else "ws"
        websocket_url = f"{current_scheme}://{request.get_host()}{ws_relative_url}"


        with connect(websocket_url) as websocket:
            data = {
                    'client': client,
                    'lawyer': lawyer,
                }
            websocket.send(json.dumps(data)) 

        return JsonResponse({'data': 'received'})