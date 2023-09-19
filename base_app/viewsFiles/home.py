from django.shortcuts import render
from django.views import View


class Home(View):

    def get(self, request):
                
        context = { }
        print(request.user)
        return render(request, 'components/home.html', context)