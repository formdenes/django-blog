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

@login_required(login_url='/accounts/login')
def ors_mypatrol(request):
    current_user = request.user
    patrol = Patrol.objects.filter(group_leader=current_user)
    members = Patrolmember.objects.filter(patrol = patrol[0])
    return render(request, 'ors/mypatrol.html',{'patrol': patrol, 'members':members})

def ors_patrol_collection(request):
    if request.method == 'POST':
        form = forms.EnterPassword(request.POST)
        if form.is_valid():
            group = form.cleaned_data['group']
            patrol = form.cleaned_data['patrol']
            pw = form.cleaned_data['password']
            ret_group = Group.objects.get(number=group)
            ret_patrol = Patrol.objects.get(group_num=ret_group, name=patrol)
            ret_pw = ret_patrol.secret
            if pw == ret_pw:
                members = Patrolmember.objects.filter(patrol = ret_patrol)
                return render(request, 'patrol_collection.html', {'patrol':patrol, 'members':members})
            else:
                message = "Hibás őrsi titok! Figyelj oda a kis- és nagybetűkre, Caps Lock használatára!"
                form2 = forms.SearchPatrol()
                return render(request, 'patrol_search.html', {'form':form2,'pwform':form, 'message_pw':message})
        else:
            message = "Nincs ilyen őrs a megadott csapatban!"
            return render (request, "patrol_search.html", {'pwform':form, 'message_search':message})
    else:
        return redirect('status')

def ors_status(request):
    if request.method == 'POST':
        form = forms.SearchPatrol(request.POST)
        if form.is_valid():
            group = form.cleaned_data['group_number']
            patrol = form.cleaned_data['patrol_name']
            try:
                ret_group = Group.objects.get(number=group)
            except:
                message = "Ebből a csapatból még senki nem regisztrált az oldalra!"
                return render(request, 'patrol_search.html', {'form':form, 'message_search': message})
            if ret_group:
                try:
                    ret_patrol = Patrol.objects.get(group_num=ret_group, name=patrol)
                except:
                    message = "Ebből a csapatból ez az őrs még nem rigsztrált az oldalra!"
                    return render(request, "patrol_search.html", {'form': form, 'message_search': message})
                if ret_patrol:
                    pwform = forms.EnterPassword({'group':ret_group.number, 'patrol':ret_patrol.name})
                    return render(request, "patrol_search.html", {'form': form, 'pwform': pwform, 'group': ret_group, 'patrol': ret_patrol})
                else:
                    message = "Ilyen őrs ebben a csapatban nem létezik!"
                    return render(request, "patrol_search.html", {'form':form, 'message_search':message})
            else:
                message = "Ebből a csapatból még senki nem regisztrált az oldalra!"
                return render(request, 'patrol_search.html', {'form':form, 'message_search': message})
        else:
            message = "Hibásan kitöltött adatok! Ellenőrizd, hogy a csapatnál csak a számot adtad-e meg!"
            return render(request, 'patrol_search.html', {'form':form, 'message_search':message})
    else:
        form = SearchPatrol()
        # megoldani, hogy legordulo listabol lehessen valasztani
    return render(request, 'patrol_search.html', {'form': form})
