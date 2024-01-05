from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import login
from ..models import Profile, User, Lawyer, Client
from ..forms import MyUserCreationForm
from django.utils.decorators import method_decorator
from ..decorators import allowed_referers, login_register_view
from ..utils.authorization import Authorization

@method_decorator(login_register_view(redirect_url="home"), name='dispatch')
class QuestionSpecialty(View):
    
    def get(self, request):
        request.session['loggingIn'] = False
        return render(request, 'components/questionSpecialty.html')
    
    def post(self, request):
        joinAs = request.POST.get("joinButton")

        if(joinAs == "Join as Lawyer"):
            request.session['isLawyer'] = True
            return redirect("register-lawyer")       

        request.session['isLawyer'] = False
        return redirect("register-client")

@method_decorator(login_register_view(redirect_url="home"), name='dispatch')
class RegisterUser(View):    

    lawyerRegister = False
    template = 'registerClient'

    def get(self, request):
        return self.renderRegisterTemplate(request)

    def post(self, request):

        form = MyUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)

            if User.objects.filter(email=user.email).exists():
                messages.error(request, 'User already exists!')
                return redirect('.')
            
            user.save()
            
            profile = Profile()
            profile.user = user
            profile.isLawyer = True if self.lawyerRegister else False
            profile.isClient = False if self.lawyerRegister else True
            profile.avatar = 'avatar.webp'

            profile.save()

            # Depending the user, we connect the profile to a Lawyer 
            # model or a Client.
            if profile.isLawyer:
                lawyer = Lawyer()
                lawyer.profile = profile
                lawyer.save()    

                login(request, user, "django.contrib.auth.backends.ModelBackend")
                Authorization.add_into_group(user, 'lawyers')
                return redirect('lawyer_info')
            else:
                client = Client()
                client.profile = profile
                client.save()  

            login(request, user, "django.contrib.auth.backends.ModelBackend")
            Authorization.add_into_group(user, 'clients')
            return redirect('home')
        else:
           errors = form.errors
           print(errors)
           for key, value in errors.items():
               messages.error(request, value)

        return self.renderRegisterTemplate(request)

    
    def renderRegisterTemplate(self, request):

        form = MyUserCreationForm()
        context = { 'form': form }

        self.template = 'registerClient' if not self.lawyerRegister else 'registerLawyer'
        
        return render(request, f'components/{self.template}.html', context)