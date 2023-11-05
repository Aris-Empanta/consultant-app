from ..models import User, Profile, Client
from .profile import BaseProfile

class BaseClient(BaseProfile):

    def get_client_by_username(self, client_username)-> Client:
        # We fetch the lawyer object using the received username.
        client_user_obj = User.objects.filter(username=client_username).first()
        client_profile_obj = Profile.objects.filter(user=client_user_obj).first()
        client = Client.objects.filter(profile=client_profile_obj).first()

        return client