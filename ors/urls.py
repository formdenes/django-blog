from django.urls import include, re_path, path
from . import views

app_name = 'ors'

urlpatterns = [
    path('mypatrol/', views.ors_mypatrol, name='mypatrol'),
    path('editpatrol/', views.ors_editpatrol, name='editpatrol'),
    path('editpatrolmembers/', views.ors_editpatrolmembers, name='editpatrolmembers'),
    path('editcollection/', views.ors_editcollection, name='editcollection'),
    path('csapatok/', views.csapatok, name='csapatok'),
    path('', views.csapatok, name='taglista'),
]
