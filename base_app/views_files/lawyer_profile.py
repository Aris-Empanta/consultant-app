from django.views import View
from django.shortcuts import redirect, render
from ..models import User

class Profile(View):
    
    def get(self, request, username):
 
        try:
            user = User.objects.get(username=username)
            avatar = user.profile.avatar
            member_since = user.date_joined
            first_name = user.first_name
            last_name = user.last_name

            context = { 'avatar': avatar, 
                        'member_since': member_since,
                        'first_name': first_name,
                        'last_name': last_name }
            # First we check if there is an authenticated user, and if his username 
            # is the same as the username in the url parameter. Then, depending if 
            # the user is a lawyer or a client, we render the appropriate template.
            if request.user.is_authenticated and request.user.username == username:
                
                if user.profile.Lawyer:             
                    return render(request, 'components/profile/editable_lawyer_profile.html', context)
                else:
                    return render(request,'components/profile/editable_client_profile.html', context)
            else:
                if user.profile.Lawyer:             
                    return render(request, 'components/profile/lawyer_profile.html', context)
                else:                                        
                    return render(request, 'components/profile/client_profile.html', context)

        except User.DoesNotExist:
            return render(request, 'components/reusable/404.html')
        except Exception as e:
            print(f'General exception: {e}')
            return render(request, 'components/reusable/500.html')        