from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Lawyer, Client, Profile, Rating, AvailableHours, Appointments, Messages
   
admin.site.register(User, UserAdmin)   
admin.site.register(Lawyer)
admin.site.register(Client)
admin.site.register(Profile)
admin.site.register(Rating)
admin.site.register(AvailableHours)
admin.site.register(Appointments)
admin.site.register(Messages)