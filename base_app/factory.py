from django_seed import Seed
from .models import User, Profile, Client, Lawyer, AvailableHours, Rating

seeder = Seed.seeder()

seeder.add_entity(User, 1, {

})


inserted_pks = seeder.execute()