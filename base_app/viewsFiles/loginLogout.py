from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User

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
            return redirect('home')
        
        return redirect('login')
        


class Logout(View):

    def get(self, request):
        logout(request)
        return redirect('home')