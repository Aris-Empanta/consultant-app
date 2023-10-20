from django.views import View
from django.shortcuts import redirect, render
from ..models import User
import urllib.parse

class Profile(View):
    
    def get(self, request, username):
        
        try:
            user = User.objects.get(username=username)
            avatar = user.profile.avatar
            member_since = user.date_joined.strftime("%b %Y")
            first_name = user.first_name
            last_name = user.last_name
            is_static = False

            # We parse the url, to get the encoded special characters (/, :, etc...)
            avatar_url = urllib.parse.unquote(avatar.url[1:])

            # we examine if the avatar's url is a file belonging to our server 
            # or a google image url. We save this info in a variable and pass it 
            # to the template through context
            if(avatar_url[0:4] != 'http'):
                is_static = True
                avatar_url = f'img/profile-pics/{avatar.url}'
            
            context = { 'avatar_url': avatar_url,
                        'member_since': member_since,
                        'first_name': first_name,
                        'last_name': last_name,
                        'username': username,
                        'is_static': is_static }
            
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
            print('user does not exist')
            return render(request, 'components/reusable/404.html')
        except Exception as e:
            print(f'General exception: {e}')
            return render(request, 'components/reusable/500.html')        