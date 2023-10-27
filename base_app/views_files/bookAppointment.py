from django.views import View
from django.http import JsonResponse
import json

class BookAppointment(View):
    def post(self, request):
        body = json.loads(request.body)
        client = request.user
        lawyer_username = body['lawyer']

        return JsonResponse({'data': 'received'})