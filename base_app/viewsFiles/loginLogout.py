from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.contrib import messages
from django.utils.decorators import method_decorator
from ..decorators import allowed_referers, login_register_view
from ..models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from ..forms import PasswordResetForm, SetPasswordForm
import os
from dotenv import load_dotenv

load_dotenv()

@method_decorator(login_register_view(redirect_url="home"), name='dispatch')
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
    
@method_decorator(login_register_view(redirect_url="home"), name='dispatch')
class PasswordResetView(PasswordResetView):
    template_name = "components/password-reset.html"
    email_template_name = "components/password-reset-email.html"
    from_email = os.getenv("EMAIL_HOST_USER")
    form_class = PasswordResetForm

@method_decorator(login_register_view(redirect_url="home"), name='dispatch')
class PasswordResetDoneView(PasswordResetDoneView):
    template_name = "components/password-reset-done.html"

@method_decorator(login_register_view(redirect_url="home"), name='dispatch')
class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "components/password-reset-confirmation.html"
    form_class = SetPasswordForm

@method_decorator(login_register_view(redirect_url="home"), name='dispatch')
class PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "components/password-reset-complete.html"

class Logout(View):

    def get(self, request):
        logout(request)
        return redirect('home')