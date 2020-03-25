from django import forms
from . import models
from taggit.forms import *

class CreateChallenge(forms.ModelForm):
    # cimkek = TagField()
    class Meta:
        model = models.Challenge
        fields = ['name', 'desc', 'thumb', 'promoted', 'tags']

class SearchChallenge(forms.Form):
    search_text = forms.CharField(label='Keresés',max_length=30)
