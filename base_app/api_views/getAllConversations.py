from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..models import Messages
from django.http import JsonResponse

@method_decorator(login_required(login_url="login"), name='dispatch')
class GetAllConversations(View):
    def get(self, request):
        user = request.user.username

        conversations = Messages.objects.filter(receiver=user).order_by('-time_sent')

        print(len(conversations))

        return JsonResponse({'conversations': 'yo'})