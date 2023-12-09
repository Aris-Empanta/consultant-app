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
from ..models import Lawyer
from django.db.models import Q

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
    def format_booked_appointments_data(self, appointments_objects_list)->list:
                
        return [ 
                  {
                    'day_name': appointment.starting_time.strftime('%A'),
                    'date': appointment.starting_time.strftime('%d/%m/%Y'),
                    'starting_time': appointment.starting_time.strftime('%H:%M'),
                    'ending_time': appointment.ending_time.strftime('%H:%M'), 
                    'first_name': appointment.client.profile.user.first_name, 
                    'last_name': appointment.client.profile.user.last_name,
                    'profile_link': f'/profile/{appointment.client.profile.user.username}',
                    'avatar': appointment.client.profile.avatar.url,
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

          if self.is_whole_number(average_rating):
              average_rating = int(average_rating)

          return f'{average_rating}/5'
        
        return 'There are no ratings yet'
    
    # This method checks if a float number can be converted to an integer.
    def is_whole_number(self, float_number):
        return int(float_number) == float_number

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
        paragraph_amount = random.randint(1, 2)

        return fake.paragraph(nb_sentences=paragraph_amount)
    
    def random_phone_number(self):
        phone =  (f'+30 69{random.randint(10, 99)} '
                  f'{random.randint(10000000, 99999999)} ')
        
        return phone
    
    def create_fake_appointments(self, lawyer):
        # We get the datetime object of tommorow noon.
        tommorow = timezone.make_aware(datetime.now() + timedelta(days=1))
        tommorow_noon = tommorow.replace(hour=12, minute=0, second=0, microsecond=0) 

        # We create appointments for the next 7 days
        for i in range(7):
            starting_time = tommorow_noon + timedelta(days=i)
            ending_time = starting_time + timedelta(hours=7)
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
        
    # the method that does the lawyer searching in the database.
    def get_lawyers_filtered(self, expertise, name_input):

        name_input = name_input.strip()
        expertise = expertise.strip()
        names = name_input.split(' ')

        first_name = ''
        last_name = ''
        valid_name = True

        # We separate first name and last name
        if len(names) == 1:
            first_name = names[0].strip()
        elif len(names) == 2:
            first_name = names[0].strip()
            last_name = names[1].strip()
        elif len(names) > 3:
            valid_name = False
        else:
            first_name = ''
            last_name = ''

        # We examine the case the user put more than 3 words in name input.
        if not valid_name:
            return Lawyer.objects.filter(Q(pk__isnull=True))
        
        # We examine the case that all fields empty.
        if self.is_empty_string(expertise) and self.is_empty_string(name_input):
            return Lawyer.objects.all()

        # We examine the case that only the area of expertise exists.
        if not self.is_empty_string(expertise) and self.is_empty_string(name_input):
            return Lawyer.objects.filter(Q(areasOfExpertise__icontains=expertise))

        # We examine the case that only the first name exists
        if self.is_empty_string(expertise) and len(names) == 1:
            return Lawyer.objects.filter(Q(profile__user__first_name__icontains=first_name))

        # We examine the case that only the first name and last name exist
        if self.is_empty_string(expertise) and len(names) == 2:
            return Lawyer.objects.filter(Q(profile__user__first_name__icontains=first_name) &
                                         Q(profile__user__last_name__icontains=last_name))                        

        # We examine the case that the area of expertise and first name exist
        if not self.is_empty_string(expertise) and len(names) == 1:
            return Lawyer.objects.filter(Q(areasOfExpertise__icontains=expertise) &
                                         Q(profile__user__first_name__icontains=first_name))

        # We examine the case that the area of expertise, first name and last name exist.
        if not self.is_empty_string(expertise) and len(names) == 2:
            return Lawyer.objects.filter(Q(areasOfExpertise__icontains=expertise) &
                                         Q(profile__user__first_name__icontains=first_name) &
                                         Q(profile__user__last_name__icontains=last_name)) 
                                          
    # The method to convert the Queryset of Lawyers we retrieved with a method above to 
    # a list of dictionaries that contain only the lawyer's info we need.
    def format_lawyers_search_results(self, lawyers)-> list:
        lawyers_data = list()

        if lawyers is not None:
            for lawyer in lawyers:
                lawyer_info = dict()

                lawyer_info['username'] = lawyer.profile.user.username
                lawyer_info['first_name'] = lawyer.profile.user.first_name
                lawyer_info['last_name'] = lawyer.profile.user.last_name
                lawyer_info['avatar'] = lawyer.profile.avatar.url
                lawyer_info['ratings'] = self.calculateAverageRating(lawyer)
                lawyer_info['city'] = lawyer.city
                lawyer_info['address'] = lawyer.address
                lawyer_info['areas_of_expertise'] = lawyer.areasOfExpertise.split(':') if lawyer.areasOfExpertise else []

                lawyers_data.append(lawyer_info)  
        
        return lawyers_data

    def is_empty_string(self, string):
        if len(string) == 0:
            return True
        else:
            return False