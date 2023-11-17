from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from ..decorators import allowed_users
import json

@method_decorator(allowed_users(allowed_roles=["clients"]), name='dispatch')
class LawyerRatings(View):
    def get(self, request):
        pass

    def post(self, request):
        body = json.loads(request.body)
        lawyer = body['lawyer']
        rating = body['rating']
        comments = body['comments']

        print(comments)

        return JsonResponse({'message': 'Your rating has been successfully submited!'})