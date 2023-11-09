from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ..models import User

@method_decorator(login_required(login_url="login"), name='dispatch')
class MessagesPage(View):
    
    def get(self, request, username):
        sender = request.user

        print(username)

        try:
            receiver = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, 'components/reusable/404.html')
        except Exception as e:
            print(f'General exception: {e}')
            return render(request, 'components/reusable/500.html')

        context = {
            'sender': sender,
            'receiver': receiver,
        }

        return render(request, 'components/messages.html', context)