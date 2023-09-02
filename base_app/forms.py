from django.forms import ModelForm, PasswordInput
from django.contrib.auth.models import User

class UserRegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username' ,'password']

        widgets = {
        'password': PasswordInput(),
        }