from django.views import View
from django.shortcuts import redirect
from ..models import User, Profile, Lawyer, Client
from django.contrib.auth import logout
from django.contrib import messages
from ..utils.authorization import Authorization
from allauth.socialaccount.models import SocialAccount
import cloudinary.uploader
from django.db import IntegrityError

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
                # We add in the session an indicator that this is a lawyer
                #  profile or not
                profile = Profile.objects.filter(user=user).first()
                if profile.isLawyer:
                    request.session['is_lawyer'] = True
                else:
                    request.session['is_lawyer'] = False
                    
                return redirect('home')
            else:
                id=user.id                
                User.objects.get(id=id).delete()
                messages.error(request, f'There is no user with email {request.user.email}!')
                logout(request)
                return redirect('login')
        
        isLawyer = False
        registerUrl = ''

        try:
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
                        return redirect(registerUrl)
            
            # The user does not exist, so we create a new Profile with that user
            profile = Profile()

            if request.user.is_authenticated:
                profile.user = request.user
                if 'isLawyer' in request.session:
                    profile.isLawyer = True if isLawyer else False
                    profile.isClient = False if isLawyer else True      
            
            # we save the url of the social account's picture as 
            # profile's avatar
            account = SocialAccount.objects.filter(user=request.user)
            social_account_avatar = account[0].extra_data.get('picture')

            # Upload the image to Cloudinary and get the public ID
            response = cloudinary.uploader.upload(social_account_avatar)

            # Save the public ID to the CloudinaryField
            profile.avatar = response['public_id']
            profile.save()       

            # Depending the user, we connect the profile to a Lawyer 
            # model or a Client, and add the corresponding group.
            if profile.isLawyer:
                lawyer = Lawyer()
                lawyer.profile = profile
                lawyer.save()  
                Authorization.add_into_group(request.user, 'lawyers')
                return redirect('lawyer_info')  
            else:
                client = Client()
                client.profile = profile
                client.save()   
                Authorization.add_into_group(request.user, 'clients')
            
            return redirect('home')
        except IntegrityError:
            # We handle the case a google registered user 
            # already exists during registration
            logout(request)
            messages.error(request, 'User already exists!')
            return redirect(registerUrl)