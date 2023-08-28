from django.shortcuts import render
from django.views.generic import ListView

# Create your views here.
class Home(ListView):
    template_name = 'home.html'
    
    def get_queryset(self):
        # Return the data you want to display as a list or queryset
        custom_data = [
            {'title': 'Item 1', 'content': 'Content 1'},
            {'title': 'Item 2', 'content': 'Content 2'},
            # Add more items as needed
        ]
        return custom_data