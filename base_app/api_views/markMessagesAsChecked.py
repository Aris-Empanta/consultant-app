from django.http import JsonResponse
from django.views import View
from ..base_classes.lawyers import BaseLawyer
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..models import Messages

@method_decorator(login_required(login_url="login"), name='dispatch')
class MarkAppointmentAsChecked(View, BaseLawyer):
    
    def patch(self, request):
        try:
            user = request.user.username

            # We mark the authenticated lawyer's appointments as checked.
            Messages.objects.filter(receiver=user).update(checked=True)
            print('correct')

            return JsonResponse({'data': 'Messages successfully marked as checked'})
        except Exception as e:
            print(f'General exception: {e}')
            return JsonResponse({'data': 'Internal server error'})