from django import forms
from . import models
from django.forms.widgets import HiddenInput, PasswordInput
from django.forms.formsets import BaseFormSet
from django.utils.translation import gettext_lazy as _


class SearchPatrol(forms.Form):
    group_number = forms.CharField(label='Csapatszám', max_length=4)
    patrol_name = forms.CharField(label='Őrs neve', max_length=25)

class EditPatrol(forms.ModelForm):
    # cimkek = TagField()
    class Meta:
        model = models.Patrol
        fields = ['name', 'group_num', 'secret']

class EditPatrolmembers(forms.ModelForm):
    class Meta:
        model = models.Patrolmember
        fields = ['nickname']

class EditPatrolmembersFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        
        nicknames = []

        for form in self.forms:
            if form.cleaned_data:
                nickname = form.cleaned_data['nickname']

                if nickname in nicknames:
                    duplicates = True
                nicknames.append(nickname)
            
            if duplicates:
                raise forms.ValidationError('Nem lehet két azonos nevű őrstag!')

class EnterPassword(forms.Form):
    password = forms.CharField(label='Őrsi titok')
    group = forms.CharField(widget=forms.HiddenInput())
    patrol = forms.CharField(widget=forms.HiddenInput())

class EditChallengeList(forms.ModelForm):
    class Meta:
        model = models.PatrolChallenge
        fields = ['challenge']
        labels = {
            'challenge': _('Kihívás')
        }

class EditChallengeListFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return

        challenges = []

        for form in self.forms:
            if form.cleaned_data:
                challenge = form.cleaned_data['challenge']

                if challenge in challenges:
                    duplicates = True
                challenges.append(challenge)

            if duplicates:
                raise forms.ValidationError(
                    'Nem lehet ugyanaz a kihívás kétszer!')

