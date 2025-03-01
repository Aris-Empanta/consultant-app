from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from ..models import Lawyer, Profile, AvailableHours
from ..forms import LawyerInfoForm
from ..enums import AreasOfExpertise
from datetime import date, datetime, timedelta
from ..utils.dates import DateUtils
from django.utils.decorators import method_decorator
from ..decorators import allowed_users
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@method_decorator(login_required(login_url="login"), name='dispatch')
@method_decorator(allowed_users(allowed_roles=["lawyers"]), name='dispatch')
class LawyerInfo(View):

    def get(self, request):

        form = LawyerInfoForm() 
        areas_of_expertise = list(map(lambda x : x.value, AreasOfExpertise))
        context = { 'form': form, 'areas_of_expertise': areas_of_expertise }
        
        return render(request, 'components/lawyer_info.html', context)
    
    def post(self, request):

        try:
            areas_of_expertise_list = request.POST.getlist("areas_of_expertise")
            areas_of_expertise = ":".join(areas_of_expertise_list)

            form = LawyerInfoForm(request.POST)
            lawyer_info = form.save(commit=False)

            profile = Profile.objects.get(user=request.user)
            lawyer = Lawyer.objects.get(profile=profile)

            # Now we save all the form data to the current logged in lawyer
            lawyer.description = lawyer_info.description
            lawyer.address = lawyer_info.address
            lawyer.areasOfExpertise = areas_of_expertise
            lawyer.hourlyRate = lawyer_info.hourlyRate
            lawyer.city = lawyer_info.city
            lawyer.lisenceStatus = lawyer_info.lisenceStatus
            lawyer.phone = lawyer_info.phone
            lawyer.yearsOfExperience = lawyer_info.yearsOfExperience

            lawyer.save()

            referring_url = request.META.get('HTTP_REFERER', None)

            if referring_url and 'lawyer_info' in referring_url:
                return redirect("lawyer_available_hours")
            
            return redirect('lawyer_available_hours')    
        except Lawyer.DoesNotExist as e:
            print(e)
        except Exception as e:
            print(e)

@method_decorator(login_required(login_url="login"), name='dispatch')
@method_decorator(allowed_users(allowed_roles=["lawyers"]), name='dispatch') 
class LawyerAvailableHours(View):
    def get(self, request):
        # We will create a dictionary that contains the current day and the 
        # remaining days of the week, in order the lawyer to choose his available
        # hours. The key will be the day's name and the key will be the day's date
        # in format DD/MM/YYYY.
        days_of_available_hours= dict()        
        todays_date = timezone.now()
        today = date.today().isoweekday()
        days_addition = 0

        for x in range(today, 8):
            day_name = DateUtils.render_day_name(x)
            date_format = (todays_date + timedelta(days=days_addition)).strftime("%d/%m/%Y")
            days_of_available_hours[f"1_{day_name}"] = date_format            
            days_addition += 1

        # We find the date of the next monday
        days_till_monday = 8-today
        next_monday_date = (todays_date + timedelta(days=days_till_monday))

        for x in range(1, 8):
            day_name = DateUtils.render_day_name(x)
            days_of_available_hours[f"2_{day_name}"] = (next_monday_date + timedelta(days=x-1)).strftime("%d/%m/%Y")

        context = {
            "days_of_available_hours": days_of_available_hours,
        }

        return render(request, 'components/lawyer-available-hours.html', context)
     
    def post(self, request):
        # We create a dictionary with only the date/time key value pairs and without the 
        # csrf token and keep only the dates in the dictionary 
        available_hours_dict = request.POST.copy()
        available_hours_dict.pop('csrfmiddlewaretoken')
        # We will need the object of the logged in lawyer later when saving the available
        #  hours / appointments
        lawyer = Lawyer.objects.get(pk=request.user.profile.lawyer.id)

        # if there are already available hours we erase them and replace with the new ones
        existing_available_hours = AvailableHours.objects.filter(lawyer=lawyer)

        if len(existing_available_hours) > 0:
            existing_available_hours.delete()

        # We loop though all the dates that have lawyer's available hours, in order
        # to validate the times given and save them to the database.
        for key, values in available_hours_dict.lists():
            # We convert the current examined date from this string format "dd/mm/yyyy" 
            # to 3 different integer variables: year, month, day, in order to construct 
            # the datetime objects later successfully, and after the validation save them 
            # to the database.
            day_month_year_list = [ int(x) for x in key.split("/") ]
            year = day_month_year_list[2]
            month = day_month_year_list[1]
            day = day_month_year_list[0]            
            
            #We create datetime objects for the starting and ending time of the interval
            starting_time_hours_and_minutes = [int(x) for x in values[0].split(":")]
            ending_time_hours_and_minutes = [int(x) for x in values[1].split(":")]
            
            starting_time_1_hours = starting_time_hours_and_minutes[0]
            starting_time_1_minutes = starting_time_hours_and_minutes[1]
            ending_time_1_hours = ending_time_hours_and_minutes[0]
            ending_time_1_minutes = ending_time_hours_and_minutes[1]

            starting_time_1 = timezone.make_aware(datetime(year, month, day, starting_time_1_hours, starting_time_1_minutes))
            ending_time_1 = timezone.make_aware(datetime(year, month, day, ending_time_1_hours, ending_time_1_minutes))

            # The ending time should be at least 1 hour after the starting time, 
            # otherwise it should return an error message
            ending_one_hour_later = starting_time_1 + timedelta(hours=1)

            if ending_one_hour_later > ending_time_1:
                error_message = "Ending times should be at least 1 hour after starting times"
                messages.error(request, error_message)
                return redirect('lawyer_available_hours')
            
            appointments_duration_1 = int(values[2])
            breaks_between_appointments_1= int(values[3])

            # The list with the appointments of the first interval
            appointments_per_interval = DateUtils.generate_appointments_per_interval(starting_time_1, 
                                                                                      ending_time_1,
                                                                                      appointments_duration_1,
                                                                                      breaks_between_appointments_1)
            # We save the intervals and the appointments in the database
            DateUtils.save_intervals_and_appointments(lawyer,
                                                      starting_time_1, 
                                                      ending_time_1 ,
                                                      appointments_per_interval)
            
            # We initialise the starting and ending time of a potential second interval
            starting_time_2 = None
            ending_time_2 = None

            #Now we handle the case the intervals in a day to be 2.
            if(len(values) > 4):
                starting_time_hours_and_minutes_2 = [int(x) for x in values[4].split(":")]
                ending_time_hours_and_minutes_2 = [int(x) for x in values[5].split(":")]
                
                starting_time_2_hours = starting_time_hours_and_minutes_2[0]
                starting_time_2_minutes = starting_time_hours_and_minutes_2[1]
                ending_time_2_hours = ending_time_hours_and_minutes_2[0]
                ending_time_2_minutes = ending_time_hours_and_minutes_2[1]

                starting_time_2 = timezone.make_aware(datetime(year, month, day, starting_time_2_hours, starting_time_2_minutes))
                ending_time_2 = timezone.make_aware(datetime(year, month, day, ending_time_2_hours, ending_time_2_minutes))
                # The second interval's starting time should not be before the first interval's ending time.
                if(starting_time_2 < ending_time_1):
                    error_message = """ 
                                        The second interval's starting time should be at the same time or 
                                        later from the starting interval's ending time
                                    """
                    messages.error(request, error_message)
                    return redirect('lawyer_available_hours')
                
                # The second intervals ending time should be at least one hour after the starting time.
                ending_2_one_hour_later = starting_time_2 + timedelta(hours=1)

                if ending_2_one_hour_later > ending_time_2:
                    error_message = "Ending times should be at least 1 hour after starting times"
                    messages.error(request, error_message)
                    return redirect('lawyer_available_hours')
                
                # If the second interval's starting time is the same as the first interval's ending time, 
                # we combine the 2 intervals in one, and empty the starting and ending time of the second 
                # interval variables.
                if(starting_time_2 == ending_time_1):
                    # We will update the ending time of this interval with the new one
                    DateUtils.update_ending_time(lawyer, ending_time_1, ending_time_2)
                    # and we remove the values from the second interval's starting/ending time
                    starting_time_2 = None
                    ending_time_2 = None
            
            #save them to the database the final intervals. Might be 2 or 1 if combined.
            if starting_time_2 is not None:
                appointments_duration_2 = int(values[6])
                breaks_between_appointments_2 = int(values[7])
                
                # The list with the appointments of the second interval
                appointments_per_second_interval = DateUtils.generate_appointments_per_interval(starting_time_2, 
                                                                                                ending_time_2,
                                                                                                appointments_duration_2,
                                                                                                breaks_between_appointments_2)
                # We save the intervals and the appointments in the database
                DateUtils.save_intervals_and_appointments(lawyer,
                                                          starting_time_2, 
                                                          ending_time_2,
                                                          appointments_per_second_interval)

        return redirect('profile', username=request.user.username)