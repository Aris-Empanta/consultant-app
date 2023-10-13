from django.http import HttpResponse
from django.shortcuts import redirect

# The following decorator will be used to restrict 
# clients or layers to access certain views.
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None

            if(request.user.groups.exists()):
                group = request.user.groups.all()[0]

            if group  in allowed_roles:
                return view_func(request, *args, **kwargs)
            else: 
                return redirect("home")
            
        return wrapper_func
    return decorator