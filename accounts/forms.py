from django import forms
from . import models
from .models import Profile

class RegisterProfileData(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['group_num', 'patrol']

# class CreateChallenge(forms.ModelForm):
#     # cimkek = TagField()
#     class Meta:
#         model = models.Challenge
#         fields = ['name', 'desc', 'thumb', 'promoted', 'add_to_patrol', 'tags']


# class AddChallengeToPatrol(forms.Form):
#     patrol = forms.CharField(widget=forms.HiddenInput())
#     challenge = forms.CharField(widget=forms.HiddenInput())


# class RemoveChallengeFromPatrol(forms.Form):
#     patrol = forms.CharField(widget=forms.HiddenInput())
#     challenge = forms.CharField(widget=forms.HiddenInput())


# class SearchChallenge(forms.Form):
#     search_text = forms.CharField(label='Keresés', max_length=30)
