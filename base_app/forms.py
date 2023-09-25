from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import User
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2'] 

class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", 
                                       "placeholder":"Email",
                                       "id": "resetPasswordEmailField"}),
    )