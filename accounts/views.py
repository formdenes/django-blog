from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from . import forms
from .forms import RegisterProfileData
from .models import Profile
from ors.models import Group, Patrol

# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            #log the user in
            login(request, user)
            form = forms.RegisterProfileData()
            return render(request, 'accounts/setdata.html', {'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form':form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            #log in the user
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form':form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def setdata_view(request):
    form = forms.RegisterProfileData()
    #todo craete template, post-get
    if request.method=='POST':
        form = RegisterProfileData(request.POST)
        if form.is_valid():
            user = request.user
            group_num = form.cleaned_data['group_num']
            patrol_name = form.cleaned_data['patrol']
            secret = form.cleaned_data['secret']
            Profile.objects.create(user=user, group_num=group_num, patrol=patrol_name, secret=secret)
            group = Group.objects.filter(number=group_num)
            #check if group exists
            if group:
                #group already exists, check patrol
                patrol = patrol.objects.filter(group_num=group, name=patrol_name)
                if patrol:
                    #patrol already exists, error
                    message="Ez az őrs már létezik ebben a csapatban!"
                    return render(request, 'accounts/setdata.html', {'form': form, 'errors': message})
                else:
                    #create patrol
                    Patrol.objects.create(name=patrol_name, group_num=group, secret=secret, group_leader=user)
                    return redirect('home')
            else:
                #create group
                new_group = Group.objects.create(number=group_num)
                Patrol.objects.create(name=patrol_name, group_num=new_group, secret=secret, group_leader=user)
            return redirect('home')
        else:
            message = form.errors
            return render(request, 'accounts/setdata.html', {'form': form, 'errors':message})
    return render(request, 'accounts/setdata.html', {'form':form})

@login_required(login_url='/accounts/login')
def profile_view(request):
    data = Profile.objects.get(user=request.user)
    form = forms.RegisterProfileData(initial={'group_num':data.group_num, 'patrol':data.patrol, 'secret':data.secret})
    return render(request, 'accounts/viewdata.html', {'form': form})
