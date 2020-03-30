from django.urls import include, re_path, path
from . import views

app_name = 'challenge'

urlpatterns = [
    path('create/', views.challenge_create, name='create'),
    path('mylist/', views.challenge_mylist, name='mylist'),
    path('list/', views.challenge_mylist, name='list'),
    path('', views.challenge_list, name='challengelist'),
]
