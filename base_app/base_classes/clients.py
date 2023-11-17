from ..models import User, Profile, Client, Appointments
from .profile import BaseProfile
from django.utils import timezone
from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()

class BaseClient(BaseProfile):

    def get_client_by_username(self, client_username)-> Client:
        # We fetch the lawyer object using the received username.
        client_user_obj = User.objects.filter(username=client_username).first()
        client_profile_obj = Profile.objects.filter(user=client_user_obj).first()
        client = Client.objects.filter(profile=client_profile_obj).first()

        return client
    
    def check_if_client_can_rate(self, request)->bool:

        client_can_rate = False

        if request.user.is_authenticated and request.user.profile.client:
            current_client = Client.objects.filter(profile=request.user.profile).first()
            client_appointments = Appointments.objects.filter(client=current_client).order_by('ending_time')
            
            # We check if the client had appointment(s) with the lawyer, and if the oldest 
            # appointment arranged has been completed.
            if len(client_appointments) > 0:
                timezone_difference = int(os.getenv('TIMEZONE_DIFFERENCE'))
                time_now =  timezone.now() + timedelta(hours=timezone_difference)
                appointment_ending_time = client_appointments[0].ending_time
            
                if(appointment_ending_time < time_now):
                    client_can_rate = True
           
        return client_can_rate