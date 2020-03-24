from django import forms
from . import models

class SearchPatrol(forms.Form):
    group_number = forms.CharField(label='Csapatszám:', max_length=4)
    patrol_name = forms.CharField(label='Őrs neve:', max_length=25)