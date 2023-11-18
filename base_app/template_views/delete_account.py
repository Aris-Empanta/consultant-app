from django.shortcuts import render
from django.contrib.auth import logout
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..models import User

@method_decorator(login_required(login_url="login"), name='dispatch')
class DeleteAccount(View):

    def get(self, request):
        return render(request, 'components/delete-account.html')
    
    def delete(self, request):
        try:
            user = User.objects.get(username=request.user.username)
            user.delete()
            logout(request)

            return JsonResponse({'deleted': True })
        except User.DoesNotExist:
                print('User does not exist')
                return JsonResponse({'deleted': False })
        except Exception as e:
            print(f'General exception in user deletion: {e}')
            return JsonResponse({'deleted': False })