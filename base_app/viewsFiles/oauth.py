from django.views import View
from django.shortcuts import redirect

class ExamineOauth(View):

    def get(self, request):

        isLawyer = request.session['isLawyer']

        if 'isLawyer' in request.session and isLawyer:
            return redirect('question-specialty')
        
        return redirect('home')