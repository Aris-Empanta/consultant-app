from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.shortcuts import redirect
from ..models import Profile
from ..forms import UserRegisterForm
import time

class QuestionSpecialty(View):
    
    def get(self, request):
        return render(request, 'components/questionSpecialty.html')
    
class RegisterUser(View):    

    lawyerRegister = False
    referer = None 
    protocol = 'http'
    template = 'registerClient'
    
    def get(self, request):

        if request.is_secure():
            self.protocol = 'https'
        else:
            self.protocol = 'http'       

        if "HTTP_REFERER" in request.META:
            self.referer = f'{request.META["HTTP_REFERER"]}'

        url = f'{ self.protocol }://{request.META["HTTP_HOST"]}'

        questionSpecialtyUrl = f'{url}/question-specialty/'
        
        if self.referer == questionSpecialtyUrl:
           return self.renderRegisterTemplate(request)
        
        return redirect("home")


    def post(self, request):
        form = UserRegisterForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            profile = Profile()
            profile.user = user

            user.save()
            profile.save()

            return redirect('successfully-registered')
        else:
           errors = form.errors

           for key, value in errors.items():
               messages.error(request, value)

        return self.renderRegisterTemplate(request)

    
    def renderRegisterTemplate(self, request):

        form = UserRegisterForm()
        context = { 'form': form }

        self.template = 'registerClient' if not self.lawyerRegister else 'registerLawyer'
        
        return render(request, f'components/{self.template}.html', context)

# MAKE IT ACCESSIBLE ONLY WITH REFERER!!!
class SuccessFullyRegistered(View):

    def get(self, request):
        
        return render(request, 'components/successfullyRegistered.html', {})