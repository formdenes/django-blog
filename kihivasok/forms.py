from django import forms
from . import models
from taggit.forms import *

class CreateChallenge(forms.ModelForm):
    cimkek = TagField()
    class Meta:
        model = models.Challenge
        fields = ['name', 'desc', 'promoted', 'thumb']
