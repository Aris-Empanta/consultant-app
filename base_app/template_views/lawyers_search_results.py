from django.shortcuts import render
from django.views import View
from ..models import Lawyer
from django.db.models import Q
from ..base_classes.lawyers import BaseLawyer
from django.core.paginator import Paginator

class LawyersSearchResults(View, BaseLawyer):
    def get(self, request):
        # These query params should exist otherwise we send the 404 page.
        expertise = request.GET.get('expertise')
        name = request.GET.get('name')
        page = request.GET.get("page")

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
            lawyer_info['address'] = lawyer.address
            lawyer_info['areas_of_expertise'] = lawyer.areasOfExpertise.split(':')

            lawyers_data.append(lawyer_info)       
        
        paginator = Paginator(lawyers_data, 6)

        # If the page of the query exceeds the existing amount, of is is less than 1,
        # we render the 404 page
        if int(page) > paginator.num_pages or int(page) < 1:
            return render(request, 'components/reusable/404.html')

        page_of_lawyers = paginator.get_page(page)

        # The variable that hold the queries except of page number, 
        # to assist the pagination links generation.
        base_queries = f'?expertise={expertise}&name={name}&page='
        current_page_obj = paginator.page(page)

        # The pages numbers
        previous_page = current_page_obj.previous_page_number() if current_page_obj.has_previous() else None
        current_page = int(page)
        next_page = current_page_obj.next_page_number() if current_page_obj.has_next() else None
        last_page = paginator.num_pages if paginator.num_pages > 1 else None

        # The pages links
        first_page_link = f'{base_queries}1'
        previous_page_link = f'{base_queries}{previous_page}' if previous_page else None
        current_page_link = f'{base_queries}{current_page}'
        next_page_link = f'{base_queries}{next_page}' if next_page else None
        last_page_link = f'{base_queries}{last_page}' if last_page else None

        #The logic of the dots between pagination links
        first_has_dots = False
        last_has_dots = False

        if current_page > 3:
            first_has_dots = True
        
        if last_page:
            if current_page < last_page - 2:
                last_has_dots = True

        context = { 
                    'lawyers_data': page_of_lawyers, 
                    'lawyers_amount': len(lawyers_data),
                    'base_queries': base_queries,
                    'paginator': paginator,
                    'first_page_link': first_page_link,
                    'current_page_obj': current_page_obj,
                    'previous_page': previous_page,
                    'previous_page_link': previous_page_link,
                    'next_page': next_page,
                    'next_page_link': next_page_link,
                    'last_page': last_page,
                    'last_page_link' : last_page_link,
                    'current_page': current_page,
                    'current_page_link': current_page_link,
                    'last_has_dots': last_has_dots,
                    'first_has_dots': first_has_dots
                   }

        return render(request, 'components/lawyers_search_results.html', context)