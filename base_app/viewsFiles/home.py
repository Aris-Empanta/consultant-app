from django.shortcuts import render
from django.views import View
from allauth.socialaccount.models import SocialApp, SocialAccount


class Home(View):

    def get(self, request):

        user = request.user

        google = SocialApp.objects.get(provider='google')
        
        referer = "empty"

        if "HTTP_REFERER" in request.META:
            referer = request.META.get('HTTP_REFERER', '')
            if 'isLawyer' in request.session and request.session['isLawyer'] is not None:
                isLawyer = request.session['isLawyer']

        context = {  "referer": referer }
        return render(request, 'components/home.html', context)