from django.shortcuts import render
from django.views import View
from django.contrib import messages
from ..models import Lawyer
from ..forms import LawyerInfoForm

class LawyerInfo(View):

    def get(self, request):

        form = LawyerInfoForm()

        areas_of_expertise = ['Criminal Law', 'Family Law']

        context = { 'form': form, 'areas_of_expertise': areas_of_expertise }
        return render(request, 'components/lawyer_info.html', context)