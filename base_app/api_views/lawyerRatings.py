from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from ..decorators import allowed_users
import json
from ..base_classes.lawyers import BaseLawyer
from ..models import Rating

@method_decorator(allowed_users(allowed_roles=["clients"]), name='dispatch')
class LawyerRatings(View, BaseLawyer):
    def get(self, request):
        pass

    def post(self, request):
        body = json.loads(request.body)
        rating = body['rating']
        comments = body['comments']
        client = request.user.profile.client
        lawyer = self.get_lawyer_by_username(body['lawyer'])

        # We check if a rating already exists for the given client and lawyer
        existing_rating = Rating.objects.filter(client=client, lawyer=lawyer).first()

        if existing_rating:
            # Update the existing rating
            existing_rating.value = rating
            existing_rating.comments = comments
            existing_rating.save()
        else:
            # Create a new rating
            new_rating = Rating(client=client, lawyer=lawyer, value=rating, comments=comments)
            new_rating.save()


        return JsonResponse({'message': 'Your rating has been successfully submited!'})