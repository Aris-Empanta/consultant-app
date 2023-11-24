from django.shortcuts import render
from django.views import View
from ..models import Lawyer
from django.db.models import Q
from ..base_classes.lawyers import BaseLawyer

class LawyersSearchResults(View, BaseLawyer):
    def get(self, request):
        # These query params should exist otherwise we send the 404 page.
        expertise = request.GET.get('expertise')
        name = request.GET.get('name')

        if expertise == None or name==None:
            return render(request, 'components/reusable/404.html')
        
        name_input = name.split(' ')

        first_name = ''
        last_name = ''

        # We separate first name and last name
        if len(name_input) == 1:
            first_name = name_input[0].strip()
        elif len(name_input) > 1:
            first_name = name_input[0].strip()
            last_name = name_input[1].strip()
        else:
            first_name = ''
            last_name = ''
        
        lawyers = Lawyer.objects.filter(
                        Q(areasOfExpertise__icontains=expertise) &
                        Q(profile__user__first_name__icontains=first_name) &
                        Q(profile__user__last_name__icontains=last_name)
                    )
        
        lawyers_data = list()

        for lawyer in lawyers:
            lawyer_info = dict()

            lawyer_info['username'] = lawyer.profile.user.username
            lawyer_info['first_name'] = lawyer.profile.user.first_name
            lawyer_info['last_name'] = lawyer.profile.user.last_name
            lawyer_info['avatar'] = self.format_avatar_link(request, lawyer.profile.avatar.url)
            lawyer_info['ratings'] = self.calculateAverageRating(lawyer)
            lawyer_info['city'] = lawyer.city
            lawyer_info['address'] = lawyer_info

            lawyers_data.append(lawyer_info)

        context = { 'lawyers_data': lawyers_data }

        return render(request, 'components/lawyers_search_results.html', context)