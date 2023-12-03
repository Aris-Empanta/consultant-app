from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..models import Messages

@method_decorator(login_required(login_url="login"), name='dispatch')
class GetUncheckedMessages(View):

    # The method to get all the unchecked messages of a user
    def get(self, request):

        # We retrieve all the booked unchecked appointments of the 
        # authenticated lawyer.
        user = request.user.username
        unchecked_messages = Messages.objects.filter(receiver=user, checked=False)
        amount = len(unchecked_messages)

        return JsonResponse({'amount': amount})