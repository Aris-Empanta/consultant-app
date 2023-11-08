from django.views import View
from django.shortcuts import render
from ..models import User, Lawyer, AvailableHours, Appointments
from ..enums import AreasOfExpertise
import urllib.parse
from ..utils.dates import DateUtils
from ..base_classes.lawyers import BaseLawyer
from ..forms import LawyerInfoForm

class Profile(View, BaseLawyer):
    
    def get(self, request, username):
        
        try:
            user = User.objects.get(username=username)
            avatar = user.profile.avatar
            member_since = user.date_joined.strftime("%b %Y")
            first_name = user.first_name
            last_name = user.last_name
            is_locally_stored = False

            # The variable that indicates if the authenticated user is a lawyer
            lawyer_authenticated = False 
            # The variable that indicates if the visited profile is the 
            # authenticated user's profile
            my_own_profile = False

            media_folder = '/media/'
            
            # We parse the url, to get the encoded special characters (/, :, etc...)
            avatar_url = urllib.parse.unquote(avatar.url).replace(media_folder, '')

            # we examine if the avatar's url is a file belonging to our server 
            # or a google image url. We save this info in a variable and pass it 
            # to the template through context
            if(not avatar_url.startswith('http') or avatar_url.startswith('/http')):
                is_locally_stored = True
                avatar_url = f'{media_folder}{avatar_url}'
            
            context = { 'avatar_url': avatar_url,
                        'member_since': member_since,
                        'first_name': first_name,
                        'last_name': last_name,
                        'username': username,
                        'is_locally_stored': is_locally_stored }
            print(avatar_url)
            
            # if the user is a lawyer, we add some extra context with the lawyer's details.
            if user.profile.Lawyer: 
                    # First we fetch the unbooked appointments of the lawyer so that a 
                    # client can choose them.
                    lawyer = Lawyer.objects.get(profile=user.profile)
                    appointments = Appointments.objects.filter(lawyer=lawyer, booked=False)
                    # We format the appointments starting and ending time:
                    formated_appointments = DateUtils.format_appointments(appointments)

                    context['description'] = lawyer.description if lawyer.description is not None else "No description available"
                    context['areasOfExpertise']  = lawyer.areasOfExpertise.split(':') if lawyer.areasOfExpertise is not None else ""
                    context['city']  = lawyer.city  
                    context['yearsOfExperience']  = lawyer.yearsOfExperience
                    context['averageRating']  = lawyer.averageRating 
                    context['hourlyRate']  = lawyer.hourlyRate  if lawyer.hourlyRate is not None else "Contact Lawyer to learn price"
                    context['address']  = lawyer.address
                    context['lisenceStatus']  = lawyer.lisenceStatus
                    context['phone']  = lawyer.phone if lawyer.phone is not None else "Not available"
                    context['lawyer_authenticated'] = lawyer_authenticated
                    context['my_own_profile'] = my_own_profile
                    context['appointments'] = formated_appointments
            

            # If there is an authenticated user and this user is a lawyer, we mention
            # it through a boolean, in order to hide the appointment button from other 
            # lawyers. Only a client can book appointments.
            if request.user.is_authenticated and request.user.profile.Lawyer:
                lawyer_authenticated = True
                context['lawyer_authenticated'] = lawyer_authenticated

            # First we check if there is an authenticated user, and if his username 
            # is the same as the username in the url parameter. Then, depending if 
            # the user is a lawyer or a client, we render the appropriate template.
            if request.user.is_authenticated and request.user.username == username:

                my_own_profile = True
                context['my_own_profile'] = my_own_profile

                if user.profile.Lawyer:  
                    available_hours = AvailableHours.objects.filter(lawyer=lawyer)   
                    booked_appointments = Appointments.objects.filter(lawyer=lawyer, booked=True).order_by('-ending_time')            
                    available_hours_list = DateUtils.format_available_hours_list(available_hours)
                    areas_of_expertise = list(map(lambda x : x.value, AreasOfExpertise))

                    context['available_hours'] = available_hours_list
                    context['lawyer_info_form'] = LawyerInfoForm()
                    context['booked_appointments'] = self.format_booked_appointments_data(request, booked_appointments)
                    context['areas_of_expertise'] = areas_of_expertise
                    
                    return render(request, 'components/profile/editable_lawyer_profile.html', context)
                else:
                    return render(request,'components/profile/client_profile.html', context)
            else:

                if user.profile.Lawyer:                      
                    return render(request, 'components/profile/lawyer_profile.html', context)
                else:                                        
                    return render(request, 'components/profile/client_profile.html', context)

        except User.DoesNotExist:
            print('user does not exist')
            return render(request, 'components/reusable/404.html')
        except Exception as e:
            print(f'General exception: {e}')
            return render(request, 'components/reusable/500.html')      