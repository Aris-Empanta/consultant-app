from django.http import JsonResponse
from django.views import View
from ..base_classes.lawyers import BaseLawyer
from ..models import Appointments

class AllBookedAppointments(View, BaseLawyer):

    def get(self, request):

        lawyer = self.get_lawyer_by_username(request.user.username)
        booked_appointments = Appointments.objects.filter(lawyer=lawyer, booked=True)

        appointments_list = [
            {
                'starting_time': appointment.starting_time ,
                'ending_time': appointment.ending_time, 
                'client_first_name': appointment.client.profile.user.first_name, 
                'client_last_name': appointment.client.profile.user.last_name,
                'checked': appointment.checked
            }
            for appointment in booked_appointments
        ]

        # Convert the list to JSON and send it as a response
        return JsonResponse({'booked_appointments': appointments_list})
