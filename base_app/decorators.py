from django.http import HttpResponse
from django.shortcuts import redirect

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
                return redirect("home")
            
        return wrapper_func
    return decorator