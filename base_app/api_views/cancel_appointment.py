from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import json
from ..utils.dates import DateUtils
from ..models import Lawyer, Appointments
from ..base_classes.profile import BaseProfile

@method_decorator(login_required(login_url="login"), name='dispatch')
class CancelAppointment(View, BaseProfile):

    def patch(self, request):
        try:
            body = json.loads(request.body)
            starting_time = DateUtils.extract_starting_time(body['starting_time'])
            
            lawyer_queryset = Lawyer.objects.filter(profile=request.user.profile)

            # The case the user is a lawyer
            if(len(lawyer_queryset) > 0):
                lawyer = request.user.profile.lawyer
                appointment = Appointments.objects.filter(lawyer=lawyer, starting_time=starting_time).first()
                receiver = appointment.client.profile.user.username

                self.cancel_appointment(appointment)
                self.inform_about_cancellation(request, receiver, lawyer)
            # The case the user is a client
            else:
                client = request.user.profile.client
                appointment = Appointments.objects.filter(client=client, starting_time=starting_time).first()
                receiver = appointment.lawyer.profile.user.username

                self.cancel_appointment(appointment)
                self.inform_about_cancellation(request, receiver, client)
                
                
            return JsonResponse({'message': 'appointment cancelled'})
        except Exception as e:
            print(f'General Exception in appointment cancellation: {e}')
            return JsonResponse({'message': 'appointment cancellation failed'})