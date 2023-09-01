from django.forms import ModelForm
from .models import Lawyers

class LawyerRegisterForm(ModelForm):
    class Meta:
        model = Lawyers
        fields = []