from django.http import JsonResponse
from django.views import View
from ..base_classes.lawyers import BaseLawyer
from ..models import Appointments
from django.utils.decorators import method_decorator
from ..decorators import allowed_users

@method_decorator(allowed_users(allowed_roles=["lawyers"]), name='dispatch')
class GetUncheckedAppointments(View, BaseLawyer):

    # The method to get all the unchecked appointments of a lawyer
    def get(self, request):

        # We retrieve all the booked unchecked appointments of the 
        # authenticated lawyer.
        lawyer_username = request.user.username
        lawyer = self.get_lawyer_by_username(lawyer_username)
        unchecked_appointments = Appointments.objects.filter(lawyer=lawyer, booked=True, checked=False)
        amount = len(unchecked_appointments)

        return JsonResponse({'amount': amount})