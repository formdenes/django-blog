from django.urls import include, re_path
from . import views

app_name = 'challenge'

urlpatterns = [
    re_path(r'^$', views.challenge_list, name='challengelist'),
]
