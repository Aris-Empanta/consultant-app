from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import User
from django import forms
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

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError("There is no user registered with the specified email address!")
        return email