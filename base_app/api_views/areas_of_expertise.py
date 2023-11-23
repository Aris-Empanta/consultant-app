from django.http import JsonResponse
from django.views import View
from ..enums import AreasOfExpertise

class AreasOfExpertiseView(View):

    def get(self, request, area):

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
