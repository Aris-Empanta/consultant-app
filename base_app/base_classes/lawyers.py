from ..models import User, Profile, Lawyer

class BaseLawyer:

    def get_lawyer_by_username(self, lawyer_username)-> Lawyer:
        # We fetch the lawyer object using the received username.
        lawyer_user_obj = User.objects.filter(username=lawyer_username).first()
        lawyer_profile_obj = Profile.objects.filter(user=lawyer_user_obj).first()
        lawyer = Lawyer.objects.filter(profile=lawyer_profile_obj).first()

        return lawyer