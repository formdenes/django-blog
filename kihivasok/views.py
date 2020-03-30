from django.shortcuts import render, redirect
from .models import Challenge, NewsPost
from ors.models import Patrol, PatrolChallenge
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from . import forms
from .forms import AddChallengeToPatrol
from django.db.models.functions import Lower
from django.db.models import Q

# Create your views here.
def challenge_list(request):
    ch = Challenge.objects.all()
    user = request.user
    if user.is_authenticated:
        patrol = Patrol.objects.get(group_leader=user)
        patrol_id = patrol.id
        if request.method == 'POST':
            form = AddChallengeToPatrol(request.POST)
            if form.is_valid():
                #addtolist
                patrol_pk = form.cleaned_data['patrol']
                patrol_inst = Patrol.objects.get(pk = patrol_pk)
                challenge_pk = form.cleaned_data['challenge']
                challenge_inst = Challenge.objects.get(pk = challenge_pk)
                addChallenge = PatrolChallenge(patrol=patrol_inst, challenge=challenge_inst)
                #check if already in list
                try:
                    addChallenge.save()
                except:
                    pass
                return render(request, 'kihivasok/challenge_list.html', {'challenge': ch, 'form': form})
        else:
            form = AddChallengeToPatrol(initial={'patrol':patrol_id})
        return render(request, 'kihivasok/challenge_list.html', {'challenge':ch, 'form':form})
    else:
        return render(request, 'kihivasok/challenge_list.html', {'challenge':ch})

@login_required(login_url='/accounts/login')
def challenge_mylist(request):
    current_user = request.user
    ch = Challenge.objects.filter(created_by = current_user)
    return render(request, 'kihivasok/challenge_mylist.html', {'challenge':ch})

@login_required(login_url="/accounts/login")
def challenge_create(request):
    if request.method == 'POST':
        form = forms.CreateChallenge(request.POST, request.FILES)
        if form.is_valid():
            #save article to db
            instance = form.save(commit=False)
            instance.created_by = request.user
            instance.save()
            form.save_m2m()
            return redirect('challenge:challengelist')
    else:
        form = forms.CreateChallenge()
    return render(request, 'kihivasok/challenge_create.html', {'form': form})

def kereses(request):
    if request.method == "POST":
        form = forms.SearchChallenge(request.POST)
        if form.is_valid():
            tags = form.cleaned_data['search_text']
            tags = tags.split()
            results = Challenge.objects.filter(tags__name__in=tags).distinct()
            # title_results = Challenge.objects.filter(name='undefined')
            # for t in tags:
            #     q1 = Challenge.objects.filter(name__contains=tags.forloop.coun)
            #     title_results.union(q1)
            # title_results = Challenge.objects.filter(name__contains=tags[0])
            # results += Challenge.objects.filter(tags__name__in=name).distinct()
            return render(request,"search_challenge.html", {'form':form, 'results':results})
        else:
            message= "Hibás keresés"
            return render(request, "search_challenge.html",{'form':form, 'message':message})
    else:
        form = forms.SearchChallenge()
    return render(request, "search_challenge.html", {'form':form})

def index(request):
    actual_news = NewsPost.objects.filter(actual=True).order_by('-timestamp')
    latest_challenges = Challenge.objects.filter(promoted = True).order_by('-timestamp')[:3]
    top_challenges = Challenge.objects.filter(promoted = True).order_by('timestamp')[:3]
    return render(request, 'kihivasok/index.html', {'actual_news':actual_news, 'latest_challenges':latest_challenges, 'top_challenges':top_challenges})


