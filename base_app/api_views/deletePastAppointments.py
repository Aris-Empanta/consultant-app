from django.views import View
from django.http import JsonResponse
from ..models import Appointments
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime,timedelta

class DeletePastAppointments(View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
     
    def delete(self, request): 
        _2_days_ago = datetime.now() - timedelta(days = 2)
        # We fetch and delete all the appointments that ended more than 2 days ago.
        try:
            past_appointments = Appointments.objects.filter(ending_time__lt=_2_days_ago)
            past_appointments.delete()

            return JsonResponse(f"{past_appointments.count()} past appointments deleted successfully.")
        except Exception as e:
            return JsonResponse(f"An error occurred while deleting past appointments: {e}")