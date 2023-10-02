from django.http import Http404
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from ..models import Lawyer, Profile
from ..forms import LawyerInfoForm
from ..enums import AreasOfExpertise

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
        return render(request, 'components/lawyer-available-hours.html')