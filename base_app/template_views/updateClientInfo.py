from django.views import View
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import allowed_users
from ..models import User
from django.db import transaction
from django.contrib import messages

@method_decorator(login_required(login_url="login"), name='dispatch')
@method_decorator(allowed_users(allowed_roles=["clients"]), name='dispatch')
class UpdateClientInfo(View):
    def post(self, request):
        first_name = request.POST.get('clientFirstName')
        last_name = request.POST.get('clientLastName')

        with transaction.atomic():
            try:
                user = User.objects.select_for_update().get(username=request.user.username)
                if(not first_name == "" and not first_name.isspace()):
                    user.first_name = first_name
                if(not last_name == "" and not last_name.isspace()):
                    user.last_name = last_name
                user.save()
            except Exception as e:
                messages.error(request, 'Unexpected error occured, please try again later')
                print(f'General exception: {e}')



        return redirect('profile', username=request.user.username)
        