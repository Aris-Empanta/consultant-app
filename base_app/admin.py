from django.contrib import admin

# Register your models here.
from .models import Lawyer, Client, Profile, Rating
   
admin.site.register(Lawyer)
admin.site.register(Client)
admin.site.register(Profile)
admin.site.register(Rating)