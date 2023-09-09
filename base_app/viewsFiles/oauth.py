from django.views import View
from django.shortcuts import render

class ExamineOauth(View):

    def get(self, request):
        
        return render(request, 'components/examine-oath.html', {})
    



    #If a profile with that email exists, redirect to the corresponding profile. If not, create a new one. 
    #so i have to search through profiles with email = googleemail