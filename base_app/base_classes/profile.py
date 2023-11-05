
class BaseProfile:

     # The flag to query if the profile's avatar is an 
     # external link or not.
    def is_avatar_external_link(self, image_link):
        is_external = False

        if image_link.startswith('http') or image_link.startswith('https'):
            is_external = True
            
        return is_external