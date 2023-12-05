from django.http import JsonResponse
from django.views import View
from ..base_classes.lawyers import BaseLawyer
from ..models import Appointments
from django.utils.timesince import timesince
from django.utils import timezone 
from django.utils.decorators import method_decorator
from ..decorators import allowed_users

@method_decorator(allowed_users(allowed_roles=["lawyers"]), name='dispatch')
class AllBookedAppointments(View, BaseLawyer):

    def get(self, request):
        lawyer = self.get_lawyer_by_username(request.user.username)
        booked_appointments = Appointments.objects.filter(lawyer=lawyer, booked=True).order_by('-time_booked')

        appointments_list = [
            {
                'day_name': appointment.starting_time.strftime('%A'),
                'date': appointment.starting_time.strftime('%d/%m/%Y'),
                'starting_time': appointment.starting_time.strftime('%H:%M'),
                'ending_time': appointment.ending_time.strftime('%H:%M'), 
                'client_first_name': appointment.client.profile.user.first_name, 
                'client_last_name': appointment.client.profile.user.last_name,
                'client_avatar': appointment.client.profile.avatar.url,
                'checked': appointment.checked,
                'time_since': timesince(appointment.time_booked, timezone.now())
            }
            for appointment in booked_appointments
        ]

        # Convert the list to JSON and send it as a response
        return JsonResponse({'booked_appointments': appointments_list})
