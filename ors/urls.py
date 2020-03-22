from django.urls import include, re_path
from . import views

app_name = 'ors'

urlpatterns = [
    re_path(r'^$', views.ors_tagok, name='taglista'),
]
