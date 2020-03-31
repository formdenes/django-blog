from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from .models import Patrol, Group, Patrolmember, PatrolChallenge
from kihivasok.models import Challenge
from django.db import transaction, IntegrityError
from django.contrib.auth.decorators import login_required
from . import forms
from .forms import SearchPatrol, EditPatrol, EditPatrolmembers, EditPatrolmembersFormSet, EditChallengeList
from kihivasok.forms import RemoveChallengeFromPatrol
from django.forms.formsets import formset_factory

# Create your views here.
def csapatok(request):
    patrols = Patrol.objects.all().order_by('group_num')
    groups = Group.objects.all().order_by('number')
    members = Patrolmember.objects.all()
    return render(request, 'ors/groups.html',{'patrols':patrols, 'groups':groups,'members':members})

@login_required(login_url='/accounts/login')
def ors_mypatrol(request):
    current_user = request.user
    patrol = Patrol.objects.filter(group_leader=current_user)
    patrol = patrol[0]
    members = Patrolmember.objects.filter(patrol = patrol)
    patrol_challenges_list = PatrolChallenge.objects.filter(patrol=patrol).values('challenge__pk')
    patrol_ch_pk = []
    for ch in patrol_challenges_list:
        patrol_ch_pk.append(ch['challenge__pk'])       
    patrol_challenges = Challenge.objects.filter(pk__in = patrol_ch_pk)
    if request.method=="POST":
        form = RemoveChallengeFromPatrol(request.POST)
        if form.is_valid():
            patrol_rec = form.cleaned_data['patrol']
            challenge_rec = form.cleaned_data['challenge']
            instance = PatrolChallenge.objects.filter(patrol=patrol_rec, challenge=challenge_rec)
            if instance:
                instance.delete()
            patrol_challenges_list = PatrolChallenge.objects.filter(patrol=patrol).values('challenge__pk')
            patrol_ch_pk = []
            for ch in patrol_challenges_list:
                patrol_ch_pk.append(ch['challenge__pk'])
            patrol_challenges = Challenge.objects.filter(pk__in=patrol_ch_pk)
            return render(request, 'ors/mypatrol.html', {'patrol': patrol, 'members': members, 'patrol_challenges': patrol_challenges, 'form': form})
        else:
            message = form.errors
            return render(request, 'ors/mypatrol.html', {'patrol': patrol, 'members': members, 'patrol_challenges': patrol_challenges, 'form': form, 'message':message})
    else:
        form = RemoveChallengeFromPatrol(initial={patrol:patrol})
    return render(request, 'ors/mypatrol.html', {'patrol': patrol,'members': members, 'patrol_challenges':patrol_challenges, 'form':form})

@login_required(login_url="/accounts/login")
def ors_editpatrol(request):
    current_user = request.user
    if request.method == 'POST':
        form_patrol = forms.EditPatrol(request.POST)
        if form_patrol.is_valid():
            #save patrol to db
            instance = form_patrol.save(commit=False)
            existing_patrol = Patrol.objects.get(group_leader=current_user)
            if existing_patrol:
                existing_patrol.name = instance.name
                existing_patrol.group_num = instance.group_num
                existing_patrol.secret = instance.secret
                existing_patrol.save()
            else:
                instance.group_leader = request.user
                instance.save()
            return redirect('ors:mypatrol')
    else:
        patrol = Patrol.objects.filter(group_leader=current_user)
        patrol = patrol[0]
        form_patrol = forms.EditPatrol(
            initial = {
                'name': patrol.name,
                'group_num':patrol.group_num,
                'secret':patrol.secret
                })
        #patrolmembers data
    return render(request, 'ors/editpatrol.html', {'form_patrol': form_patrol})

@login_required(login_url="/accounts/login")
def ors_editpatrolmembers(request):
    member_formset = formset_factory(EditPatrolmembers, extra=1, max_num=20, can_delete=True)
    current_user = request.user
    patrol = Patrol.objects.filter(group_leader=current_user)
    patrol = patrol[0]
    members = Patrolmember.objects.filter(patrol=patrol)
    if  request.method == 'POST':
        form_members = member_formset(request.POST)
        if form_members.is_valid():
            patrol_members = []
            existing_nicknames = []
            for member_form in form_members:
                nickname = member_form.cleaned_data.get('nickname')
                to_delete = member_form.cleaned_data.get('DELETE') 
                if nickname and not to_delete:
                    if nickname in existing_nicknames:
                        error_message = 'Nem szerepelhet két egyforma nevű őrstag!'
                        return render(request, 'ors/editpatrolmembers.html', {'form_members': form_members, 'error': error_message})
                    existing_nicknames.append(nickname)
                    patrol_members.append(Patrolmember(patrol=patrol, nickname=nickname))                    
            try:
                with transaction.atomic():
                    Patrolmember.objects.filter(patrol=patrol).delete()
                    Patrolmember.objects.bulk_create(patrol_members)
                    members = Patrolmember.objects.filter(patrol=patrol).order_by('nickname')
                    form_members = member_formset(initial=members.values())
                    return render(request, 'ors/editpatrolmembers.html', {'form_members':form_members})
            except IntegrityError:
                messages.error(request,'Sajnos valami hiba történt!')
                return render(request, 'ors/editpatrolmembers.html', {'form_members':form_members})
        else:
            error_message = form_members.errors
            return render(request,'ors/editpatrolmembers.html', {'form_members':form_members, 'error':error_message})
    else:
        form_members = member_formset(initial=members.values())
    return render(request, 'ors/editpatrolmembers.html', {'form_members':form_members})
    
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
            ret_challenges = PatrolChallenge.objects.filter(patrol = ret_patrol)
            if pw == ret_pw:
                members = Patrolmember.objects.filter(patrol = ret_patrol).order_by('nickname')
                return render(request, 'patrol_collection.html', {'patrol':patrol, 'members':members, 'challenges':ret_challenges})
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
                    message = "Ebből a csapatból ez az őrs még nem regisztrált az oldalra!"
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
