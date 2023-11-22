from django.core.management.base import BaseCommand
from ...factory.fake_users import FakeUsers
from ...factory.fake_ratings import FakeRatings

class Command(BaseCommand):
    def handle(self, *args, **options):
        # First we create clients and lawyers
        users = FakeUsers(2, 2)
        users.create()

        # Then the lawyers' ratings
        ratings = FakeRatings()
        ratings.generate()
