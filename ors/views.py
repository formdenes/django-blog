from django.shortcuts import render, redirect
from .models import Patrol, Group, Patrolmember
from django.contrib.auth.decorators import login_required
#from . import forms

# Create your views here.
def ors_tagok(request):
    patrols = Patrol.objects.all().order_by('group_num')
    groups = Group.objects.all().order_by('number')
    members = Patrolmember.objects.all()
    return render(request, 'ors/ors_tagok.html',{'patrols':patrols, 'groups':groups,'members':members})
