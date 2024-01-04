from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import resolve
import os
from dotenv import load_dotenv
import sys 

load_dotenv()

# The decorator below restricts the access of certain pages 
# if the user is logged in.
def login_register_view(redirect_url):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            if request.user.is_authenticated:
                return redirect(redirect_url)
            else:
                return view_func(request, *args, **kwargs)
        return wrapper_func
    return decorator

# The following decorator will be used to restrict 
# clients or layers to access certain views.
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None

            if not request.user.is_authenticated:
                return JsonResponse({'data': 'login'})

            if request.user.groups.exists():
                group = str(request.user.groups.all()[0])

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else: 
                return render(request, "components/reusable/403.html")
            
        return wrapper_func
    return decorator

# This decorator is to restrict the access to the view except there 
# are specific referer urls.  In the referers argument we have
# to put the url names of all allowed referers.
def allowed_referers(referers=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

                referer = request.META.get("HTTP_REFERER", None)
                protocol = "https"

                url = f'{ protocol }://{request.META["HTTP_HOST"]}'
                
                # we get the referer's url name (if exists)
                if referer:
                    referer = resolve(referer.replace(url, "")).url_name
                    
                if referer in referers:
                    sys.stdout.write(f'Referer is: {referer} ok')
                    return view_func(request, *args, **kwargs)
                else:
                    sys.stdout.write(f'Referer is: {referer} ok')
                    return render(request, "components/reusable/400.html")
                
        return wrapper_func
    return decorator

# The decorator that prevents api access without api key
def api_key_required():
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            api_key = request.headers.get('Api-Key')         

            if api_key == os.getenv('API_KEY'):
                return view_func(request, *args, **kwargs)
            else:
                response_data = {
                                    'error': 'Forbidden',
                                    'message': 'You do not have permission to access this resource.',
                                }
                return JsonResponse(response_data, status=403)
        return wrapper_func        
    return decorator