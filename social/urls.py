from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from . import views

app_name = 'social'

urlpatterns = [
    path('', views.social_login_view, name='soclogin'),
]