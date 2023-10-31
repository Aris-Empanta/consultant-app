from django.shortcuts import render
from django.views import View

class Home(View):

    def get(self, request):
        if request.user.is_authenticated:
            print(request.session['is_lawyer'])
        return render(request, 'components/home.html')