from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.shortcuts import redirect
from ..models import Profile
from ..forms import UserRegisterForm


class QuestionSpecialty(View):
    
    def get(self, request):
        return render(request, 'components/questionSpecialty.html')

class RegisterClient(View):    

    protocol = 'http'   
    referer = None 
    
    def get(self, request):

        if request.is_secure():
            self.protocol = 'https'
        else:
            self.protocol = 'http'       

        if "HTTP_REFERER" in request.META:
            self.referer = f'{request.META["HTTP_REFERER"]}'

        url = f'{self.protocol }://{request.META["HTTP_HOST"]}/question-specialty/'
        
        if self.referer == url:
            form = UserRegisterForm()
            context = { 'form': form}
            return render(request, 'components/registerClient.html', context)
        
        return redirect("home")


    def post(self, request):
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            profile = Profile()
            profile.user = user

            user.save()
            profile.save()
            return redirect('login')
        else:
           errors = form.errors

           for key, value in errors.items():
               messages.error(request, value)
        
        return redirect('register-client')
    
class RegisterLawyer(View):

    protocol = 'http'   
    referer = None 
    
    def get(self, request):

        if request.is_secure():
            self.protocol = 'https'
        else:
            self.protocol = 'http'       

        if "HTTP_REFERER" in request.META:
            self.referer = f'{request.META["HTTP_REFERER"]}'

        url = f'{self.protocol }://{request.META["HTTP_HOST"]}/question-specialty/'
        
        if self.referer == url:
            form = UserRegisterForm()
            context = { 'form': form}
            return render(request, 'components/registerLawyer.html', context)
        
        return redirect("home")

    def post(self, request):
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            profile = Profile()
            profile.user = user

            user.save()
            profile.save()
            return redirect('login')
        else:
           errors = form.errors

           for key, value in errors.items():
               messages.error(request, value)
        
        return redirect('register-lawyer')