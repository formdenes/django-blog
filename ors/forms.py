from django import forms
from . import models
from django.forms.widgets import HiddenInput, PasswordInput

class SearchPatrol(forms.Form):
    group_number = forms.CharField(label='Csapatszám', max_length=4)
    patrol_name = forms.CharField(label='Őrs neve', max_length=25)

class EnterPassword(forms.Form):
    password = forms.CharField(label='Őrsi titok')
    group = forms.CharField(widget=forms.HiddenInput())
    patrol = forms.CharField(widget=forms.HiddenInput())