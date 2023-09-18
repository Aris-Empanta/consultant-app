from django.views import View
from django.shortcuts import redirect
from ..models import User, Profile
from django.contrib.auth import logout
from django.contrib import messages

# The view class that does all the validation/configurations 
# after the user authenticates via oauth and returns to the 
# app. May either proceed to Home page, create profile at the 
# same time or even decide that the user is duplicate, delete
#  the user and destroy the authentication token.
class OauthHandler(View):

    def get(self, request):

        user = request.user
        #We check if this is the logging in page for google. 
        # If there is not profile with that user and it is 
        # the first registration, we raise an error.
        if 'loggingIn' in request.session and request.session['loggingIn']:
            if Profile.objects.filter(user=user).exists():
                return redirect('home')
            else:
                id=user.id                
                User.objects.get(id=id).delete()
                messages.error(request, f'There is no user with email {request.user.email}!')
                logout(request)
                return redirect('login')
        
        isLawyer = False
        registerUrl = ''
        # With the use of session, we know if the pre-register page 
        # was for a client or a lawyer.
        if 'isLawyer' in request.session:
            isLawyer = request.session['isLawyer']
            registerUrl = 'register-lawyer' if isLawyer else 'register-client' 

        # The current user's email should be unique. If it 
        # exists more than once , we logout and erase the user.
        if user.is_authenticated:            
                amount = User.objects.filter(email=user.email)

                #We check if that user exists.
                if amount.exists() and amount.count() > 1:                
                    id=user.id
                    logout(request)
                    User.objects.get(id=id).delete()
                    messages.error(request, 'User already exists!')
                    #we delete the session variable
                    if 'isLawyer' in request.session:
                        del request.session['isLawyer']
                    return redirect(registerUrl)
        
        # The user does not exist, so we create a new Profile with that user
        profile = Profile()

        if request.user.is_authenticated:
            profile.user = request.user
            if 'isLawyer' in request.session:
                profile.Lawyer = True if isLawyer else False
                profile.Client = False if isLawyer else True       
                     
        profile.save()        

        #we delete the session variable
        if 'isLawyer' in request.session:
            del request.session['isLawyer']
        
        return redirect('home')