import json
import asyncio
from websockets import connect
from django.http import JsonResponse
from django.views import View
from ..models import Appointments
from ..utils.dates import DateUtils
from django.db import transaction
from ..base_classes.lawyers import BaseLawyer 
from ..base_classes.clients import BaseClient
from django.utils import timezone
from django.utils.decorators import method_decorator
from ..decorators import allowed_users

@method_decorator(allowed_users(allowed_roles=["clients"]), name='dispatch')
class BookAppointment(View, BaseLawyer, BaseClient):

    def patch(self, request):

        body = json.loads(request.body)
        client_username = request.user.username
        lawyer_username = body['lawyer']
        appointment_date_and_time = body['appointment_date_and_time']

        # We fetch the lawyer object using the received username.
        lawyer = self.get_lawyer_by_username(lawyer_username)
        client = self.get_client_by_username(client_username)

        # We received the appointment's day via body, starting and ending 
        # time in a string format. We will extract from it the date and starting time,
        # and convert it to datetime object.
        starting_time = DateUtils.extract_starting_time(appointment_date_and_time)

        # Now we treat the following operation as a whole, and we lock the database
        # transactions to avoid concurrent bookings with the select_for_update() method.
        with transaction.atomic():
            try:
                appointment = Appointments.objects.select_for_update().get(lawyer=lawyer, starting_time=starting_time)
                
                if not appointment.booked:
                    # Client books the appointment
                    appointment.booked = True
                    appointment.client = client
                    appointment.time_booked = timezone.now()
                    appointment.save()

                    # Once the appointment gets booked, we send notification to the lawyer user via 
                    # websockets, in order to update in real time his/her booked appointments.
                    ws_relative_url = "/ws/book-appointment/"
                    current_scheme = "wss" if request.is_secure() else "ws"
                    websocket_url = f"{current_scheme}://{request.get_host()}{ws_relative_url}"

                    asyncio.run(self.send_websocket_data(websocket_url, client_username, lawyer_username))
                    return JsonResponse({'data': 'Booked!'})
                else:
                    return JsonResponse({'data': 'This Appointment has been already booked'})

            except Appointments.DoesNotExist:
                return JsonResponse({'data': 'Appointment not found'})

            except Exception as e:
                print(f'General exception: {e}')
                return JsonResponse({'data': 'Internal error occured, please try again later'})
            
    # The method to send the appointment booking notification to the websocket consumer
    async def send_websocket_data(self, websocket_url, client, lawyer):
            async with connect(websocket_url) as websocket:
                data = {
                    'client': client,
                    'lawyer': lawyer,
                }
                await websocket.send(json.dumps(data))