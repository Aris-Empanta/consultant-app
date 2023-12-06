from typing import Any
from django.views import View
from django.shortcuts import render
from ..models import User, Lawyer, AvailableHours, Appointments
from ..enums import AreasOfExpertise
import urllib.parse
from ..utils.dates import DateUtils
from ..base_classes.lawyers import BaseLawyer
from ..base_classes.clients import BaseClient
from ..forms import LawyerInfoForm
from datetime import datetime

class Profile(View, BaseLawyer, BaseClient):

    def __init__(self):
        self.lawyer_authenticated = False 
        self.my_own_profile = False
        self.media_folder = '/media/'
        self.avatar_is_locally_stored = False    
        self.can_rate_lawyer = False

    def get(self, request, username):
        
        try:
            user = User.objects.get(username=username)
            avatar = user.profile.avatar
            member_since = user.date_joined.strftime("%b %Y")
            first_name = user.first_name
            last_name = user.last_name          
            
            # We parse the url, to get the encoded special characters (/, :, etc...)
            avatar_url = urllib.parse.unquote(avatar.url).replace(self.media_folder, '')

            # we examine if the avatar's url is a file belonging to our server 
            # or a google image url. We save this info in a variable and pass it 
            # to the template through context
            if(not avatar_url.startswith('http') or avatar_url.startswith('/http')):
                self.avatar_is_locally_stored = True
                avatar_url = f'{self.media_folder}{avatar_url}'
            
            context = { 
                        'avatar_url': avatar_url,
                        'member_since': member_since,
                        'first_name': first_name,
                        'last_name': last_name,
                        'username': username,
                        'is_locally_stored': self.avatar_is_locally_stored,
                        'can_rate_lawyer':  self.can_rate_lawyer
                       }
            
            # If the profile belongs to a lawyer we add some extra details to the context.
            if user.profile.isLawyer: 
                    # First we fetch the unbooked appointments of the lawyer so that a 
                    # client can choose them.
                    lawyer = Lawyer.objects.get(profile=user.profile)
                    appointments = Appointments.objects.filter(lawyer=lawyer, 
                                                               booked=False, 
                                                               starting_time__gt = datetime.now()).order_by('starting_time')
                    # We format the appointments starting and ending time:
                    formated_appointments = DateUtils.format_appointments(appointments)

                    context['description'] = lawyer.description if lawyer.description is not None else "No description available"
                    context['areasOfExpertise']  = lawyer.areasOfExpertise.split(':') if lawyer.areasOfExpertise else []
                    context['city']  = lawyer.city  
                    context['yearsOfExperience']  = lawyer.yearsOfExperience
                    context['hourlyRate']  = lawyer.hourlyRate  if lawyer.hourlyRate is not None else "Contact Lawyer to learn price"
                    context['address']  = lawyer.address
                    context['lisenceStatus']  = lawyer.lisenceStatus
                    context['phone']  = lawyer.phone if lawyer.phone is not None else "Not available"
                    context['lawyer_authenticated'] = self.lawyer_authenticated
                    context['my_own_profile'] = self.my_own_profile
                    context['appointments'] = formated_appointments
                    context['ratings'] = self.calculateAverageRating(lawyer)
            
            # If there is an authenticated user and this user is a lawyer, we mention
            # it through a boolean, in order to hide the appointment button from other 
            # lawyers. Only a client can book appointments.
            if request.user.is_authenticated and request.user.profile.isLawyer:
                self.lawyer_authenticated = True
                context['lawyer_authenticated'] = self.lawyer_authenticated

            # First we check if there is an authenticated user, and if his username 
            # is the same as the username in the url parameter. Then, depending if 
            # the user is a lawyer or a client, we render the appropriate template.
            if request.user.is_authenticated and request.user.username == username:
                self.my_own_profile = True
                context['my_own_profile'] = self.my_own_profile

                # The case I logged in as a lawyer:
                if user.profile.isLawyer:  
                    available_hours = AvailableHours.objects.filter(lawyer=lawyer, starting_time__gt = datetime.now())   
                    booked_appointments = Appointments.objects.filter(lawyer=lawyer, 
                                                                      booked=True, 
                                                                      starting_time__gt = datetime.now()).order_by('-ending_time')            
                    available_hours_list = DateUtils.format_available_hours_list(available_hours)
                    areas_of_expertise = list(map(lambda x : x.value, AreasOfExpertise))

                    context['available_hours'] = available_hours_list
                    context['lawyer_info_form'] = LawyerInfoForm()
                    context['booked_appointments'] = self.format_booked_appointments_data(booked_appointments)
                    context['areas_of_expertise'] = areas_of_expertise
                    
                    return render(request, 'components/profile/editable_lawyer_profile.html', context)
                # The case I logged in as a client:
                else:
                    context['client_booked_appointments'] = self.get_client_appointments(request)
                    return render(request,'components/profile/client_profile.html', context)
            # The case someone (logged in or not) checks a random profile 
            # (belonging to someone else if logged in)
            else:
                if user.profile.isLawyer:  
                    # If the logged in user is a client we examine if he /she has a recent 
                    # appointment and can rate the lawyer.    
                    self.can_rate_lawyer = self.check_if_client_can_rate(request)
                    context['can_rate_lawyer'] = self.can_rate_lawyer

                    return render(request, 'components/profile/lawyer_profile.html', context)
                else:                                        
                    return render(request, 'components/profile/client_profile.html', context)

        except User.DoesNotExist:
            print('user does not exist')
            return render(request, 'components/reusable/404.html')
        except Exception as e:
            print(f'General exception in Profile: {e}')
            return render(request, 'components/reusable/500.html')      