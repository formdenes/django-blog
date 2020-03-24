from django.shortcuts import render, redirect
from .models import Challenge
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from . import forms

# Create your views here.
def challenge_list(request):
    ch = Challenge.objects.all()
    # tags = Challenge.tags()
    return render(request, 'kihivasok/challenge_list.html', {'challenge':ch})

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
