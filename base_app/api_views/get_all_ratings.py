from django.views import View
from django.http import JsonResponse
from ..models import Rating
from ..base_classes.lawyers import BaseLawyer

class GetAllRatings(View, BaseLawyer):
    
    def get(self, request, username):
        lawyer = self.get_lawyer_by_username(username)
        ratings_queryset = Rating.objects.filter(lawyer=lawyer)
        ratings_list = list()    

        for rating in ratings_queryset.iterator():
            rating_dictionary = dict()

            rating_dictionary['first_name'] = rating.client.profile.user.first_name
            rating_dictionary['last_name'] = rating.client.profile.user.last_name
            rating_dictionary['avatar'] = self.format_avatar_link(request, rating.client.profile.avatar.url)
            rating_dictionary['value'] = rating.value
            rating_dictionary['comment'] = rating.comments

            ratings_list.append(rating_dictionary)

        return  JsonResponse({'all_ratings': ratings_list})