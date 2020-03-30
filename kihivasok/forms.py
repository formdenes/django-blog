from django import forms
from . import models
from ors.models import PatrolChallenge
from taggit.forms import *

class CreateChallenge(forms.ModelForm):
    # cimkek = TagField()
    class Meta:
        model = models.Challenge
        fields = ['name', 'desc', 'thumb', 'promoted', 'add_to_patrol','tags']

class AddChallengeToPatrol(forms.Form):
    patrol = forms.CharField(widget=forms.HiddenInput())
    challenge = forms.CharField(widget=forms.HiddenInput())

class SearchChallenge(forms.Form):
    search_text = forms.CharField(label='Keresés',max_length=30)
