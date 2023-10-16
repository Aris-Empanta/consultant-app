from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import resolve

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

            if(request.user.groups.exists()):
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
                protocol = "http"

                if request.is_secure():
                    protocol = 'https' 

                url = f'{ protocol }://{request.META["HTTP_HOST"]}'
                
                # we get the referer's url name (if exists)
                if referer:
                    referer = resolve(referer.replace(url, "")).url_name

                if referer in referers:
                    return view_func(request, *args, **kwargs)
                else:
                    return render(request, "components/reusable/403.html")
        return wrapper_func
    return decorator