from django.shortcuts import render
from django.views import View


class Home(View):

    def get(self, request):
        #User.objects.all().delete()
        context = { "navbar_color" : "green" }
        return render(request, 'components/home.html', context)