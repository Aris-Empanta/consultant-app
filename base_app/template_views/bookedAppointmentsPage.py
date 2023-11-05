from django.shortcuts import render
from django.views import View
from ..base_classes.lawyers import BaseLawyer
from ..models import Appointments
from django.utils.decorators import method_decorator
from ..decorators import allowed_users

@method_decorator(allowed_users(allowed_roles=["lawyers"]), name='dispatch')
class BookedAppointmentsPage(View, BaseLawyer):
    def get(self, request):

        lawyer = self.get_lawyer_by_username(request.user.username)
        booked_appointments = Appointments.objects.filter(lawyer=lawyer, booked=True).order_by('-time_booked')

        
        return render(request, "components/booked_appointments.html")