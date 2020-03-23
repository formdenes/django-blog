from django.urls import include, re_path, path
from . import views

app_name = 'challenge'

urlpatterns = [
    path('create/', views.challenge_create, name='create'),
    path('', views.challenge_list, name='challengelist'),
]
