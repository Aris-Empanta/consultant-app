from django.shortcuts import render
from django.views import View
from ..enums import AreasOfExpertise

class Home(View):

    def get(self, request):
        # user can search though one or none areas of expertise and one name
        return render(request, 'components/home.html')