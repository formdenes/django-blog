from django.shortcuts import render, redirect
from .models import Challenge, NewsPost
from accounts.models import Profile
from ors.models import Patrol, PatrolChallenge
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from . import forms
from .forms import AddChallengeToPatrol
from django.db.models.functions import Lower
from django.db.models import Q, Count

# Create your views here.
def challenge_list(request):
    ch = Challenge.objects.filter(promoted=True)
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
            creator = Profile.objects.get(user=request.user)
            instance.creator = creator
            instance.save()
            form.save_m2m()
            return redirect('challenge:challengelist')
    else:
        form = forms.CreateChallenge()
    return render(request, 'kihivasok/challenge_create.html', {'form': form})

def kereses(request):
    user = request.user
    form_challenge = forms.AddChallengeToPatrol()
    form_search = forms.SearchChallenge()
    if user.is_authenticated:
        patrol = Patrol.objects.get(group_leader=user)
        patrol_id = patrol.id
        if request.method == 'POST' and 'add' in request.POST:
            form_challenge = AddChallengeToPatrol(request.POST)
            if form_challenge.is_valid():
                #addtolist
                patrol_pk = form_challenge.cleaned_data['patrol']
                patrol_inst = Patrol.objects.get(pk=patrol_id)
                challenge_pk = form_challenge.cleaned_data['challenge']
                challenge_inst = Challenge.objects.get(pk=challenge_pk)
                addChallenge = PatrolChallenge(
                    patrol=patrol_inst, challenge=challenge_inst)
                is_there = PatrolChallenge.objects.filter(patrol=patrol_inst, challenge=challenge_inst)
                #check if already in list
                if not is_there:
                    addChallenge.save()
                # search part
                keywords = request.POST.get('keywords')
                tags = keywords.split()
                q_object = Q(name__icontains=tags[0])
                for item in tags:
                    q_object.add(Q(name__icontains=item) |
                                 Q(desc__icontains=item), Q.OR)
                q_object.add(Q(tags__name__in=tags), Q.OR)
                queryset = Challenge.objects.filter(q_object).distinct()
                results = queryset
                form_search = forms.SearchChallenge(initial={'search_text':keywords})
                return render(request, 'search_challenge.html', {'form_search':form_search,'results':results, 'form_challenge':form_challenge})
                # return HttpResponseRedirect(request.path_info)
        elif request.method == "POST" and 'search' in request.POST:
            form_search = forms.SearchChallenge(request.POST)
            if form_search.is_valid():
                tags = form_search.cleaned_data['search_text']
                tags = tags.split()
                q_object = Q(name__icontains=tags[0])
                for item in tags:
                    q_object.add(Q(name__icontains=item) | Q(desc__icontains=item), Q.OR)
                q_object.add(Q(tags__name__in=tags), Q.OR)
                queryset = Challenge.objects.filter(q_object).distinct().exclude(promoted=False)
                results = queryset
                return render(request, "search_challenge.html", {'form_search': form_search, 'results': results, 'form_challenge':form_challenge})
            else:
                message = form_search.errors
                return render(request, "search_challenge.html", {'form_search': form_search, 'message': message, 'form_challenge':form_challenge})
        else:
            form_challenge = AddChallengeToPatrol(initial={'patrol': patrol_id})
        return render(request, 'search_challenge.html', {'form_search': form_search, 'form_challenge': form_challenge})
    else:
        if request.method == "POST":
            form_search = forms.SearchChallenge(request.POST)
            if form_search.is_valid():
                tags = form_search.cleaned_data['search_text']
                tags = tags.split()
                results = Challenge.objects.filter(tags__name__in=tags).distinct()
                # title_results = Challenge.objects.filter(name='undefined')
                # for t in tags:
                #     q1 = Challenge.objects.filter(name__contains=tags.forloop.coun)
                #     title_results.union(q1)
                # title_results = Challenge.objects.filter(name__contains=tags[0])
                # results += Challenge.objects.filter(tags__name__in=name).distinct()
                return render(request, "search_challenge.html", {'form_search': form_search, 'results': results})
            else:
                message = "Hibás keresés"
                return render(request, "search_challenge.html", {'form_search': form_search, 'message': message})
        else:
            form_search = forms.SearchChallenge()
    return render(request, "search_challenge.html", {'form_search':form_search})

def tag_search(request):
    tag_form = forms.SearchChallenge(request.POST)
    if tag_form.is_valid():
        tags = tag_form.cleaned_data['search_text']
        tags = tags.split()
        results = Challenge.objects.filter(tags__name__in=tags).distinct()
        return render(request, 'search_challenge.html', {'form_search':tag_form, 'results':results})
    else:
        return redirect('index')

def index(request):
    actual_news = NewsPost.objects.filter(actual=True).order_by('-timestamp')
    # top_challenges = Challenge.objects.annotate(ch_count=Count('id')).order_by('-ch_count')[:3]
    top_challenges_query = PatrolChallenge.objects.values('challenge__name', 'challenge__pk').annotate(c=Count('id')).order_by('-c')[:3]
    top_challenges_pk = []
    for item in top_challenges_query:
        top_challenges_pk.append(item['challenge__pk'])
    top_challenges = Challenge.objects.filter(pk__in=top_challenges_pk)
    latest_challenges = Challenge.objects.filter(promoted = True).order_by('timestamp')[:3]
    user = request.user
    if user.is_authenticated:
        patrol = Patrol.objects.filter(group_leader=user)
        if patrol:
            patrol_id = patrol[0].id
        if request.method == 'POST':
            form = AddChallengeToPatrol(request.POST)
            if form.is_valid():
                #addtolist
                patrol_pk = form.cleaned_data['patrol']
                patrol_inst = Patrol.objects.get(pk=patrol_pk)
                challenge_pk = form.cleaned_data['challenge']
                challenge_inst = Challenge.objects.get(pk=challenge_pk)
                addChallenge = PatrolChallenge(
                    patrol=patrol_inst, challenge=challenge_inst)
                #check if already in list
                try:
                    addChallenge.save()
                except:
                    pass
                return render(request, 'kihivasok/index.html', {'actual_news':actual_news, 'latest_challenges':latest_challenges, 'top_challenges':top_challenges, 'form': form})
        else:
            if patrol:
                form = AddChallengeToPatrol(initial={'patrol': patrol_id})
                return render(request, 'kihivasok/index.html', {'actual_news':actual_news, 'latest_challenges':latest_challenges, 'top_challenges':top_challenges, 'form': form})
            return render(request, 'kihivasok/index.html', {'actual_news': actual_news, 'latest_challenges': latest_challenges, 'top_challenges': top_challenges})
    else:
        return render(request, 'kihivasok/index.html', {'actual_news':actual_news, 'latest_challenges':latest_challenges, 'top_challenges':top_challenges})


