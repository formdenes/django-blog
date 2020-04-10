from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def social_login_view(request):
    return render(request, 'social/social_login.html')