from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import login
from ..models import Profile, User
from ..forms import MyUserCreationForm

class QuestionSpecialty(View):
    
    def get(self, request):
        return render(request, 'components/questionSpecialty.html')
    
    def post(self, request):
        joinAs = request.POST.get("joinButton")

        if(joinAs == "Join as Lawyer"):
            request.session['isLawyer'] = True
            return redirect("register-lawyer")       

        request.session['isLawyer'] = False
        return redirect("register-client")

    
class RegisterUser(View):    

    lawyerRegister = False
    referer = None 
    protocol = 'http'
    template = 'registerClient'
    
    def get(self, request):

        # Below there is a mechanism so that this page is only accessible 
        # through the referer page "question-specialty"
        if request.is_secure():
            self.protocol = 'https'
        else:
            self.protocol = 'http'       

        if "HTTP_REFERER" in request.META:
            self.referer = f'{request.META["HTTP_REFERER"]}'

        url = f'{ self.protocol }://{request.META["HTTP_HOST"]}'

        questionSpecialtyUrl = f'{url}/question-specialty/'
        examinOauthUrl = f'{url}/examine-oauth/'
        
        if self.referer == questionSpecialtyUrl or examinOauthUrl:
           return self.renderRegisterTemplate(request)
        
        return redirect("home")


    def post(self, request):

        form = MyUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)

            if User.objects.filter(email=user.email).exists():
                messages.error(request, 'User already exists!')
                return redirect('.')
            
            profile = Profile()
            profile.user = user
            profile.Lawyer = True if self.lawyerRegister else False
            profile.Client = False if self.lawyerRegister else True
            
            user.save()
            profile.save()

            login(request, user)
            return redirect('home')
        else:
           errors = form.errors

           for key, value in errors.items():
               messages.error(request, value)

        return self.renderRegisterTemplate(request)

    
    def renderRegisterTemplate(self, request):

        form = MyUserCreationForm()
        context = { 'form': form }

        self.template = 'registerClient' if not self.lawyerRegister else 'registerLawyer'
        
        return render(request, f'components/{self.template}.html', context)