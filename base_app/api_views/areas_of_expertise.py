from django.http import JsonResponse
from django.views import View
from ..enums import AreasOfExpertise
from django.views.decorators.csrf import csrf_exempt
import json

class AreasOfExpertiseView(View):

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        body = json.loads(request.body)
        area = body['areaOfExpertise']

        areas_of_expertise = list(map(lambda x : x.value, AreasOfExpertise))

        if area == 'all':
            return JsonResponse({'areas': areas_of_expertise})
        elif area == 'none':
            return JsonResponse({'areas': 'none'})
        else:
            specific_areas_of_expertise = list()

            for area_of_expertise in areas_of_expertise:
                if area.lower() in area_of_expertise.lower():
                    specific_areas_of_expertise.append(area_of_expertise)

            return JsonResponse({'areas': specific_areas_of_expertise})
        



from django.http import JsonResponse
from django.views import View
import time

class Scheduler(View):
    def get(self, request):

        while True:
            print('hey')
            time.sleep(1)

        return JsonResponse({'res': 'daemon stopped'})
