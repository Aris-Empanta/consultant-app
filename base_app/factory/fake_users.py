from ..models import User, Profile, Client, Lawyer
from faker import Faker
from faker.providers.person.en import Provider
import os
from dotenv import load_dotenv
from django.db import transaction
from ..base_classes.lawyers import BaseLawyer
import random

load_dotenv()

class FakeUsers(BaseLawyer):

    def __init__(self, clients_amount, lawyers_amount ):
        if not isinstance(clients_amount, int) or not isinstance(lawyers_amount, int):
            raise ValueError("clients_amount and lawyers_amount must be integers.")
         
        self.clients_amount = clients_amount
        self.lawyers_amount = lawyers_amount
        self.total_amount = clients_amount + lawyers_amount
        self.maximum_amount = 6000

    def create(self):
                
        fake = Faker()

        # We fetch the list of all the first names that exist in the faker library. 
        # We will use them to create users' first names, usernames, and emails 
        # (because unique emails of this library are a small amount)
        faker_first_names = list(set(Provider.first_names))

        # The unique first names of this library are 6824, so we can mass create 
        # users of smaller amount than this.
        if self.total_amount > self.maximum_amount:
            raise ValueError('You can produce up to 6000 fake users.')

        # We slice the first names list of Faker library to the amount given by 
        # the command.
        first_names = faker_first_names[0:self.total_amount]
        
        for i in range(self.total_amount):
            try:
                with transaction.atomic():
                    user = User.objects.create(
                        email=f'fake_{first_names[i].lower()}@fakemail.com',
                        username=f'fake_{first_names[i].lower()}',
                        first_name = first_names[i],
                        last_name = fake.last_name(),
                        password= os.getenv('FAKE_USER_PASS'),
                    )

                    profile = Profile.objects.create(
                        user = user,
                        avatar = 'avatar.webp',
                        isLawyer = False if i < self.clients_amount else True,
                        isClient = False if i >= self.clients_amount else True,
                    )

                    if i < self.clients_amount:
                        client = Client.objects.create(
                            profile=profile,
                        )
                    else:
                        lawyer = Lawyer.objects.create(
                            profile=profile,
                            areasOfExpertise = self.random_areas_of_expertise(),
                            city = fake.city(),
                            yearsOfExperience = random.randint(1, 10),
                            description = self.random_description(),
                            hourlyRate = random.randint(10, 100),
                            address = fake.address(),
                            lisenceStatus = 'active',
                            phone = self.random_phone_number(),
                        )
                        # Then we create appointments for the fake lawyer
                        self.create_fake_appointments(lawyer)

            except Exception as e:
                raise Exception(f'General exception: {e}')