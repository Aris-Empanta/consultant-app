import json
import asyncio
from websockets import connect
from django.http import JsonResponse
from django.views import View
from ..models import Lawyer, Appointments
from ..utils.dates import DateUtils

class BookAppointment(View):
    def post(self, request):
        body = json.loads(request.body)
        client = request.user.username

        # FETCH THE LAWYER OBJECT!!!



        appointment_date_and_time = body['appointment_date_and_time']

        # We received via body the appointments day, starting and ending 
        # time in a string format. We will extract from it the date and starting time,
        # and convert it to datetime object.
        starting_time = DateUtils.extract_starting_time(appointment_date_and_time)

        #Now with the starting time and the lawyer's name we find the appointment row.
        appointment = Appointments.objects.filter(lawyer=lawyer, starting_time=starting_time)[0]

        #We convert the appointment booked value to true
        appointment.booked = True
        appointment.save()

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