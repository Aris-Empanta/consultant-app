from django.core.management.base import BaseCommand
from ...factory import create_users

class Command(BaseCommand):
    def handle(self, *args, **options):
        create_users()
