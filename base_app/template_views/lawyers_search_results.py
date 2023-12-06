from django.shortcuts import render
from django.views import View
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
        
        # We retrieve a Queryset of Lawyer objects based on the user input data
        lawyers = self.get_lawyers_filtered(expertise, name)     
           
        # We modify the Queryset we retrieved to a list of dictionaries with 
        # all the data we need. 
        lawyers_data = self.format_lawyers_search_results(lawyers)     

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