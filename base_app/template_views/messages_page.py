from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ..models import User, Messages
from django.db.models import Q
from ..base_classes.profile import BaseProfile
from urllib.parse import unquote 

@method_decorator(login_required(login_url="login"), name='dispatch')
class MessagesPage(View, BaseProfile):
    
    def get(self, request, username):
        try:
            user = request.user
            conversation_partner = User.objects.get(username=username)

            # We fetch the messages that we sent to the receiver and the 
            # receiver send to us sorted by date.
            messages = Messages.objects.filter(Q(sender=user, receiver=conversation_partner.username) 
                                               | Q(sender=conversation_partner, receiver=user.username)
                                               ).order_by('time_sent')
          
            # We create an array of dictionaries for the template context, 
            # with all the data modifications needed.
            final_messages = list()

            for message in messages:
                message_dict = dict()
                message_dict['sender_username'] = message.sender.username
                message_dict['sender_avatar'] = message.sender.profile.avatar.url
                message_dict['message'] = message.message
                message_dict['time_sent'] = message.time_sent.strftime('%d/%m/%Y %H:%M')
                final_messages.append(message_dict)

            context = {
                       'user': user,
                       'conversation_partner': conversation_partner,
                       'messages': final_messages
                      }

            return render(request, 'components/messages.html', context)
        except User.DoesNotExist:
            return render(request, 'components/reusable/404.html')
        except Exception as e:
            print(f'General exception: {e}')
            return render(request, 'components/reusable/500.html')