from django.shortcuts import redirect
from django.views import View
from ..models import Profile
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from pathlib import Path

@method_decorator(login_required(login_url="login"), name='dispatch')
class UpdateProfilePic(View):
    def post(self, request):
        new_avatar = request.FILES.get('profile_pic')
        profile = Profile.objects.filter(user=request.user).first()

        # Get the path to the previous avatar using the Path object
        previous_avatar_path = Path(profile.avatar.path)

        if previous_avatar_path.exists():
            previous_avatar_path.unlink()  # Delete the previous avatar file
            print(f"File {previous_avatar_path} has been deleted.")
        else:
            print(f"File {previous_avatar_path} does not exist.")

        # Save the newly received image as the profile pic
        profile.avatar = new_avatar
        profile.save()

        return redirect('profile', username=request.user.username)
