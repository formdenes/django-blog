from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Patrol, Group, Patrolmember
from django.contrib.auth.decorators import login_required
from . import forms
from .forms import SearchPatrol

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

def ors_collection(request):
    return 'ide kellene egy jelszó, majd egy kilistázás'

@login_required(login_url="/accounts/login")
def ors_search(request):
    if request.method == 'POST':
        form = forms.SearchPatrol(request.POST)
        if form.is_valid():
            group = form.cleaned_data['group_number']
            patrol = form.cleaned_data['patrol_name']
            ret_group = Group.objects.filter(number=group)
            ret_patrol = Patrol.objects.filter(group_num = ret_group,name=patrol)
            return render (request, "orsok.html", {'gr_num':ret_group, 'p_name':ret_patrol})
            # return redirect('ors:collection')
        else:
            return HttpResponse('Hibás adatok!')
    else:
        form = SearchPatrol()
    return render(request, 'orsok.html', {'form': form})
