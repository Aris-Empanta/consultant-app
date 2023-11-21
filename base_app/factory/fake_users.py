from ..models import User, Profile, Client, Lawyer
from faker import Faker
from faker.providers.internet.en_US import InternetProvider
from faker.providers.person.en import Provider
import os
from dotenv import load_dotenv

load_dotenv()

class FakeUsers:

    def __init__(self, clients_amount, lawyers_amount ):
        if not isinstance(clients_amount, int) or not isinstance(lawyers_amount, int):
            raise ValueError("clients_amount and lawyers_amount must be integers.")
         
        self.clients_amount = clients_amount
        self.lawyers_amount = lawyers_amount
        self.total_amount = clients_amount + lawyers_amount

    def create(self):
        #   Show error if the amount requested is larger than the fakers has.

        fake = Faker()

        # All the first names and emails of the faker library to make 
        first_names = list(set(Provider.first_names))
        fake.add_provider(InternetProvider)

        # Get a list of email addresses available in the InternetProvider
        email_list = [fake.ascii_safe_email() for _ in range(100)]
        first_names_list = first_names[0:10]


        for i in range(4):

            user = User.objects.create(
                email=email_list[i],
                username=f'fake_{first_names_list[i]}',
                first_name = first_names_list[i],
                last_name = fake.last_name(),
                password= os.getenv('FAKE_USER_PASS'),
            )

            profile = Profile.objects.create(
                user = user,
                isLawyer = False if i < 3 else True,
                isClient = False if i >= 3 else True,
            )

            if i < 3:
                client = Client.objects.create(
                    profile=profile
                )
            else:
                lawyer = Lawyer.objects.create()