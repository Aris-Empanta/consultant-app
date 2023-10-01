from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from .models import User, Lawyer
from django import forms
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2'] 

class LawyerInfoForm(ModelForm):

    hourlyRate = forms.IntegerField()
    class Meta:
        model = Lawyer
        fields = ["city", "yearsOfExperience", "hourlyRate", "address", "lisenceStatus", "phone", "description"]
        labels = {
            "city": "City",
            "yearsOfExperience": _("Years of experience"),
            "hourlyRate": _("Your Hourly Rate (EUR)"),
            "address": "Address",
            "lisenceStatus": "Your lisence status",
            "phone": "Phone",
            "description": "Your profile description"
        }
        

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
    
class SetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 
                                          "class": "setNewPasswordFormField",
                                          "placeholder": "New Password"}),
    )
    new_password2 = forms.CharField(
        label=_("Confirm new password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 
                                          "class": "setNewPasswordFormField",
                                          "placeholder": "Confirm New Password"}),
    )