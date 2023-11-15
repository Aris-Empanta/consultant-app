from django.views import View
from django.http import JsonResponse
from ..models import Appointments

class DeletePastAppointments(View):
    def get(self, request): 
        appointments = Appointments.objects.all()

        return JsonResponse({'appointments': 'appointments deleted'})