from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate


# Create your views here.
class Home(View):
    def get(self, request):
        return render(request, 'components/home.html')
    
class Login(View):
    def get(self, request):
        return render(request, 'components/login.html')
    
    def post(self, request):
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'Email OR password does not exit')
            return

        user = authenticate(email=email, password=password)