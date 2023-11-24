from django.shortcuts import render
from django.views import View
from ..enums import AreasOfExpertise

class Home(View):

    def get(self, request):
        return render(request, 'components/home.html')