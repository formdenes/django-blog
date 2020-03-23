from django.urls import include, re_path, path
from . import views

app_name = 'challenge'

urlpatterns = [
    path('*', views.challenge_list, name='challengelist'),
]
