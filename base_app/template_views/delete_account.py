from django.shortcuts import render
from django.contrib.auth import logout
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from ..models import User
from pathlib import Path
from ..base_classes.profile import BaseProfile

@method_decorator(login_required(login_url="login"), name='dispatch')
class DeleteAccount(View, BaseProfile):

    def get(self, request):
        return render(request, 'components/delete-account.html')
    
    def delete(self, request):
        try:
            user = User.objects.get(username=request.user.username)

            # We delete the user's profile pic file.
            profile = user.profile
            previous_avatar_path = Path(profile.avatar.path)

            # We delete the previous avatar file (only if it is not avatar.png)
            if previous_avatar_path.exists() and not profile.avatar.name == self.default_profile_pic_name:
                previous_avatar_path.unlink()  
                print(f"File {previous_avatar_path} has been deleted.")
            else:
                print(f"File {previous_avatar_path} does not exist.")

            # We delete the user object
            user.delete()
            logout(request)

            return JsonResponse({'deleted': True })
        except User.DoesNotExist:
                print('User does not exist')
                return JsonResponse({'deleted': False })
        except Exception as e:
            print(f'General exception in user deletion: {e}')
            return JsonResponse({'deleted': False })