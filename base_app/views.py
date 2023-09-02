from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from .forms import UserRegisterForm
from .models import Profile

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
        form = UserRegisterForm()
        context = { 'form': form}
        return render(request, 'components/register.html', context)

    def post(self, request):
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            profile = Profile()
            profile.user = user
            lawyerOrClient = request.POST.get("lawyerOrClient")

            if lawyerOrClient == "lawyer":
                profile.isLawyer = True

            user.save()
            profile.save()
            return redirect('login')
        else:
           pass
        
        return redirect('register')