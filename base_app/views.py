from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

# Create your views here.
class Home(View):

    def get(self, request):
        return render(request, 'components/home.html')
    
class Login(View):

    def get(self, request):
        return render(request, 'components/login.html')
    
    def post(self, request):
        email = request.POST["email"].lower()
        password = request.POST["password"]

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'Email OR password does not exit')
            return

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            redirect('home')

class Logout(View):

    def get(self, request):
        logout(request)
        redirect('home')

class Register(View):

    def get(self, request):
        return render(request, 'components/register.html')