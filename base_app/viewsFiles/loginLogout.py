from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages
from ..models import User
from django.contrib.auth.hashers import make_password

class Login(View):

    def get(self, request):
        request.session['loggingIn'] = True
        return render(request, 'components/login.html', {})
    
    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)        

        if user is not None:
            login(request, user, "django.contrib.auth.backends.ModelBackend")
            return redirect('home')
        
        messages.error(request, 'Email or password do not match a user!')        
        return redirect('login')

class Logout(View):

    def get(self, request):
        logout(request)
        return redirect('home')