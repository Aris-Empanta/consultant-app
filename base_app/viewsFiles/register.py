from django.shortcuts import render
from django.views import View
from django.contrib import messages
from django.shortcuts import redirect
from django.db import IntegrityError
from ..models import Profile
from ..forms import MyUserCreationForm
from django.db import transaction

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
        
        if self.referer == questionSpecialtyUrl:
           return self.renderRegisterTemplate(request)
        
        return redirect("home")


    def post(self, request):

        form = MyUserCreationForm(request.POST)
        
        if form.is_valid():
                    try:
                        with transaction.atomic():
                            user = form.save(commit=False)
                            profile = Profile()
                            profile.user = user
                            profile.Lawyer = True if self.lawyerRegister else False
                            profile.Client = False if self.lawyerRegister else True
                            
                            user.save()
                            profile.save()

                        return redirect('successfully-registered')
                    except IntegrityError as e:
                        # Handle database integrity error here
                        print(f"Database error: {e}")
                        messages.error(request, "A database error occurred.")
                    except Exception as e:
                        # Handle other exceptions here
                        print(f"An error occurred: {e}")
                        messages.error(request, "An error occurred while processing your request.")
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

# MAKE IT ACCESSIBLE ONLY WITH REFERER!!!
class SuccessFullyRegistered(View):

    def get(self, request):
        
        return render(request, 'components/successfullyRegistered.html', {})