from django.shortcuts import render, redirect
from .models import Challenge
from taggit.models import Tag
from django.contrib.auth.decorators import login_required

# Create your views here.
def challenge_list(request):
    ch = Challenge.objects.all()
    # tags = Challenge.tags()
    return render(request, 'kihivasok/challenge_list.html', {'challenge':ch})
