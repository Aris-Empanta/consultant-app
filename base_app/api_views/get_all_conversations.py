from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..models import Messages
from django.http import JsonResponse
from ..base_classes.profile import BaseProfile
from django.utils.timesince import timesince
from django.utils import timezone 

@method_decorator(login_required(login_url="login"), name='dispatch')
class GetAllConversations(View, BaseProfile):

    def get(self, request):
        user = request.user.username

        # We keep only the latest message sent from each user
        conversations = Messages.objects.filter(receiver=user).order_by('-time_sent')

        conversations_list = list()

        for i in range(len(conversations)):
            
            if i == 0:
                self.append_conversation(request, conversations[i], conversations_list)
            else:
                sender_exists = any( x['sender'] == conversations[i].sender.username for x in conversations_list)

                if(sender_exists):
                    continue

                self.append_conversation(request, conversations[i], conversations_list)

        return JsonResponse({'conversations': conversations_list})
    
    def append_conversation(self, request, conversation_object, conversations_list):
        conversation_dict = dict()        
        avatar_url = conversation_object.sender.profile.avatar.url

        conversation_dict['sender'] = conversation_object.sender.username
        conversation_dict['time_sent'] = timesince(conversation_object.time_sent, timezone.now())
        conversation_dict['message'] = conversation_object.message
        conversation_dict['avatar'] = avatar_url
        conversation_dict['read'] = conversation_object.read

        conversations_list.append(conversation_dict)