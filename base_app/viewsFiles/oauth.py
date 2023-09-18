from django.views import View
from django.shortcuts import redirect
from ..models import User, Profile
from django.contrib.auth import logout
from django.contrib import messages

class ExamineOauth(View):

    def get(self, request):

        user = request.user
        #We check if this is the logging in page for google. 
        # If there is not profile with that user and it is 
        # the first registration, we raise an error.
        if 'loggingIn' in request.session and request.session['loggingIn']:
            del request.session['loggingIn']
            if Profile.objects.filter(user=user).exists():
                return redirect('home')
            else:
                id=user.id                
                User.objects.get(id=id).delete()
                messages.error(request, f'There is no user with email {request.user.email}!')
                logout(request)
                return redirect('login')
        
        isLawyer = False
        # With the use of session, we know if the pre-register page 
        # was for a client or a lawyer.
        if 'isLawyer' in request.session:
            isLawyer = request.session['isLawyer']

        registerUrl = 'register-client' 

        if 'isLawyer' in request.session:
            registerUrl = 'register-lawyer' if isLawyer else 'register-client'       

        # The current user's email should be unique. If it 
        # exists more than once , we logout and erase the user.
        if user.is_authenticated:            
                amount = User.objects.filter(email=user.email)

                if amount.exists() and amount.count() > 1:                
                    id=user.id
                    logout(request)
                    User.objects.get(id=id).delete()
                    messages.error(request, 'User already exists!')
                    return redirect(registerUrl)
        
        # We check if a profile with our user exists. If 
        # it doesn't, we create one.
        if not Profile.objects.filter(user=user).exists():
            profile = Profile()
            profile.user = user
            if 'isLawyer' in request.session:
                profile.Lawyer = True if isLawyer else False
                profile.Client = False if isLawyer else True    
                #we delete the session variable
                del request.session['isLawyer']        
            profile.save()        
        
        return redirect('home')