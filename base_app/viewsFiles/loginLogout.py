from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages
from ..models import User

class Login(View):

    def get(self, request):
        request.session['loggingIn'] = True
        return render(request, 'components/login.html', {})
    
    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Email does not exist')
            return redirect('login')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        
        return redirect('login')

class Logout(View):

    def get(self, request):
        logout(request)
        return redirect('home')