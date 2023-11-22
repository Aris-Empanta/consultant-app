from ..models import Rating, Lawyer, Client
from faker import Faker 
import random

class FakeRatings:
    # A method that adds up to 20 ratings for all lawyers.
    def generate(self):
        lawyers = Lawyer.objects.all()

        for lawyer in lawyers.iterator():
            ratings_amount = random.randint(1,20)
            clients = Client.objects.all()

            for i in range(ratings_amount):
                random_client = random.choice(clients)

                rating = Rating.objects.create(
                    client=random_client,
                    lawyer=lawyer,
                    value=random.randint(1,5),
                    comments=self.random_comment()
                )

    def random_comment(self):
        fake = Faker()
        paragraph_amount = random.randint(1, 3)

        return fake.paragraph(nb_sentences=paragraph_amount)
