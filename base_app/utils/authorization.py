from django.contrib.auth.models import Group
from ..models import User

class Authorization:
    
    @staticmethod
    def add_into_group(user, group):
        # We check if the group exists. if not, create it. 
        try:
            group = Group.objects.get(name=group)
        except Group.DoesNotExist:
            group = Group.objects.create(name=group)
        except Exception as e:
            print(f'General Exception: {e}')

        # We check if the user belongs to that group. if not,
        #  we add he into it.
        if group not in user.groups.all():
            try:
                group.user_set.add(user)
            except Exception as e:
                print(f'General Exception: {e}')
        