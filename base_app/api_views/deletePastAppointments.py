from django.views import View
from django.http import JsonResponse
from ..models import Appointments
from django.views.decorators.csrf import csrf_exempt

class DeletePastAppointments(View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
     
    def delete(self, request): 
        appointments = Appointments.objects.all()
        print(request.headers.get('Api-Key'))

        return JsonResponse({'message': 'appointments deleted'})