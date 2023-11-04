from django.http import JsonResponse
from django.views import View
from ..models import Appointments
from ..base_classes.lawyers import BaseLawyer

class MarkAppointmentAsChecked(View, BaseLawyer):
    
    def patch(self, request):
        try:
            lawyer= self.get_lawyer_by_username(request.user.username)

            # We mark the authenticated lawyer's appointments as checked.
            Appointments.objects.filter(lawyer=lawyer, booked=True, checked=False).update(checked=True)

            return JsonResponse({'data': 'Appointments successfully marked as checked'})
        except Exception as e:
            print(f'General exception: {e}')
            return JsonResponse({'data': 'Internal server error'})