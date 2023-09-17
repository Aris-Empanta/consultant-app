from django.views import View
from django.shortcuts import redirect
from ..models import User, Profile
from django.contrib.auth import logout
from django.contrib import messages

class ExamineOauth(View):

    def get(self, request):

        isLawyer = False
        # With the use of session, we know if the pre-register page 
        # was for a client or a lawyer.
        if 'isLawyer' in request.session:
            isLawyer = request.session['isLawyer']

        registerUrl = 'register-client' 

        if 'isLawyer' in request.session:
            registerUrl = 'register-lawyer' if isLawyer else 'register-client'    

        user = request.user

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
        existingProfile = Profile.objects.filter(user=user)            

        if existingProfile.count() == 0:
            profile = Profile()
            profile.user = user
            if 'isLawyer' in request.session:
                profile.Lawyer = True if isLawyer else False
                profile.Client = False if isLawyer else True            
            profile.save()        
        
        return redirect('home')