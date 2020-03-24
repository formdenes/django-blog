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

def ors_challenge_list(request):
    patrols = Patrol.objects.all()
    members = Patrolmember.objects.all()
    return render(request, 'orsok.html',{'patrols':patrols, 'members':members})

@login_required(login_url='/accounts/login')
def ors_mypatrol(request):
    current_user = request.user
    patrol = Patrol.objects.filter(group_leader=current_user)
    members = Patrolmember.objects.filter(patrol = patrol[0])
    return render(request, 'ors/mypatrol.html',{'patrol': patrol, 'members':members})
