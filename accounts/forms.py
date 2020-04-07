from django import forms
from . import models
from .models import Profile

class RegisterProfileData(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['group_num', 'patrol', 'secret']
