from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from ..models import Lawyer, Profile
from ..forms import LawyerInfoForm
from ..enums import AreasOfExpertise
from datetime import date, datetime, timedelta
from ..helpers.dates import render_day_name

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

            return redirect("lawyer_available_hours")

        except Lawyer.DoesNotExist:

            raise Http404("Lawyer not found")

        except Exception as e:
            print(e)

class LawyerAvailableHours(View):
     
     def get(self, request):
        # We will create a dictionary that contains the current day and the 
        # remaining days of the week, in order the lawyer to choose his available
        # hours. The key will be the day's name and the key will be the day's date
        # in format DD/MM/YYYY.
        current_week = dict()
        
        todays_date = date.today()

        today = date.today().isoweekday()

        days_addition = 0

        for x in range(today, 8):
            day_name = render_day_name(x)
            date_format = (todays_date + timedelta(days=days_addition)).strftime("%d/%m/%Y")
            current_week[day_name] = date_format            
            days_addition += 1

        # We find the date of the next monday
        days_till_monday = 8-today
        next_monday_date = (todays_date + timedelta(days=days_till_monday))

        # We will create a dictionary that contains all the days and dates of the next week. 
        next_week = dict()

        for x in range(1, 8):
            day_name = render_day_name(x)
            next_week[day_name] = (next_monday_date + timedelta(days=x-1)).strftime("%d/%m/%Y")

        print(next_week)
        context = {
            "current_week": current_week,
            "next_week": next_week,
        }

        return render(request, 'components/lawyer-available-hours.html', context)