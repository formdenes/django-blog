from django.urls import include, re_path, path
from . import views

app_name = 'ors'

urlpatterns = [
    path('mypatrol/', views.ors_mypatrol, name='mypatrol'),
    path('', views.ors_tagok, name='taglista'),
]
