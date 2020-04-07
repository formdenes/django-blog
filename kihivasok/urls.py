from django.urls import include, re_path, path
from . import views
from .views import ChallengeDetailView

app_name = 'challenge'

urlpatterns = [
    path('create/', views.challenge_create, name='create'),
    path('mylist/', views.challenge_mylist, name='mylist'),
    path('list/', views.challenge_list, name='list'),
    path('<slug:slug>', ChallengeDetailView.as_view(), name='challenge_detail'),
    path('tagsearch/', views.tag_search, name='tagsearch'),
    path('', views.challenge_list, name='challengelist'),
]
