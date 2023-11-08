from django.views import View
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..models import User
from django.db import transaction
from django.contrib import messages

@method_decorator(login_required(login_url="login"), name='dispatch')
class UpdateUserFullname(View):
    def post(self, request):
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')

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
        