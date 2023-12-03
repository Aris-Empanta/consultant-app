from django.views import View
from django.http import JsonResponse
from ..models import Appointments
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime,timedelta
from django.core.mail import send_mail
import os
from dotenv import load_dotenv
from django.utils.decorators import method_decorator
from ..decorators import api_key_required

load_dotenv()

@method_decorator(api_key_required(), name='dispatch')
class RemindAppointments(View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def post(self, request):
        # We fetch the appointments that start 3 hours from now and the client
        #  has not been informed.
        now = datetime.now()
        _3_hours_later = now + timedelta(hours = 3)
        upcoming_appointments = Appointments.objects.filter(starting_time__gte=now,
                                                            starting_time__lte=_3_hours_later,
                                                            booked=True,
                                                            informed_client=False)

        for appointment in upcoming_appointments:
            if appointment.informed_client == False:
                client_email = appointment.client.profile.user.email
                mail_sent = self.remind_client(client_email, appointment)
                print(mail_sent)

        return JsonResponse({'message': 'appointments reminded'})
    
    def remind_client(self, email, appointment):
        try:
            lawyer_first_name = appointment.lawyer.profile.user.first_name
            lawyer_last_name = appointment.lawyer.profile.user.last_name
            appointment_time = appointment.starting_time.strftime("%H:%M")


            subject = 'APPOINTMENT REMINDER'
            message = f'We confirm the appointment you have today with Mr. {lawyer_first_name} {lawyer_last_name} on {appointment_time}'
            from_email = os.getenv('EMAIL_HOST_USER')
            recipient_list = [email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            # mark informed_client as True
            appointment.informed_client = True
            appointment.save()

            return 'Mail successfully sent'
        except Exception as e:
            return f'Mail exception {e}'