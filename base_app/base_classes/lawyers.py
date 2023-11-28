from ..models import User, Profile, Lawyer, Rating
from .profile import BaseProfile
from django.utils import timezone
from django.utils.timesince import timesince
from functools import reduce
import math
from ..enums import AreasOfExpertise
import random
from faker import Faker
from django.utils import timezone
from datetime import datetime, timedelta
from ..utils.dates import DateUtils

class BaseLawyer(BaseProfile):

    # This method takes a lawyer's username and returns its Queryset.
    def get_lawyer_by_username(self, lawyer_username)-> Lawyer:
        # We fetch the lawyer object using the received username.
        lawyer_user_obj = User.objects.filter(username=lawyer_username).first()
        lawyer_profile_obj = Profile.objects.filter(user=lawyer_user_obj).first()
        lawyer = Lawyer.objects.filter(profile=lawyer_profile_obj).first()

        return lawyer
    
    # This method takes a list of appointments object, and creates a context from 
    # their fields with all the info needed to be rendered.
    def format_booked_appointments_data(self,  request, appointments_objects_list)->list:
                
        return [ 
                  {
                    'day_name': appointment.starting_time.strftime('%A'),
                    'date': appointment.starting_time.strftime('%d/%m/%Y'),
                    'starting_time': appointment.starting_time.strftime('%H:%M'),
                    'ending_time': appointment.ending_time.strftime('%H:%M'), 
                    'first_name': appointment.client.profile.user.first_name, 
                    'last_name': appointment.client.profile.user.last_name,
                    'profile_link': f'/profile/{appointment.client.profile.user.username}',
                    'avatar': self.format_avatar_link(request, appointment.client.profile.avatar.name),
                    'checked': appointment.checked,
                    'time_since': timesince(appointment.time_booked, timezone.now())
                  } 
                  for appointment in appointments_objects_list
                ] 
    # The method to calculate the average rating if ratings exist.
    def calculateAverageRating(self, lawyer):
        ratings_queryset = Rating.objects.filter(lawyer=lawyer)

        if len(ratings_queryset) > 0:
          ratings = list(map(lambda x : x.value , ratings_queryset))
          average_rating = math.ceil((reduce(lambda x, y : x + y, ratings) / len(ratings)) * 10) / 10

          return average_rating
        
        return 'There are no ratings yet'
    
    # The methods below create random data for the Lawyer model, to be used in 
    # the fake objects production.
    def random_areas_of_expertise(self):
        all_areas_of_expertise = list(map(lambda x: x.value,AreasOfExpertise))
        # We create a list of random values from areas_of_expertise list that has 
        # a random length between 1 and 5 values.
        list_length = random.randint(1, 5)
        areas_of_expertise = random.sample(all_areas_of_expertise, list_length)

        areas_of_expertise_concatonated = ':'.join(areas_of_expertise)

        return areas_of_expertise_concatonated
    
    def random_description(self):
        fake = Faker()
        paragraph_amount = random.randint(1, 5)

        return fake.paragraph(nb_sentences=paragraph_amount)
    
    def random_phone_number(self):
        phone =  (f'+30 69{random.randint(10, 99)} '
                  f'{random.randint(10000000, 99999999)} ')
        
        return phone
    
    def create_fake_appointments(self, lawyer):
        # We get the datetime object of tommorow noon.
        tommorow = timezone.make_aware(datetime.now() + timedelta(days=1))
        tommorow_noon = tommorow.replace(hour=12, minute=0, second=0, microsecond=0) 

        starting_time = tommorow_noon
        ending_time = starting_time + timedelta(hours=6)
        duration = 45
        breaks = 15

        appointments = DateUtils.generate_appointments_per_interval(starting_time, 
                                                                    ending_time,
                                                                    duration,
                                                                    breaks)
        # We save the available hours and the appointments in the database
        DateUtils.save_intervals_and_appointments(lawyer,
                                                  starting_time, 
                                                  ending_time,
                                                  appointments)