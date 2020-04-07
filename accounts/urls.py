from django.conf.urls import url
from django.urls import path, re_path
from . import views

app_name = 'accounts'

urlpatterns = [
    re_path(r'^signup/$', views.signup_view, name='signup'),
    re_path(r'^setdata/$', views.setdata_view, name='setdata'),
    re_path(r'^profile/$', views.profile_view, name='profile'),
    re_path(r'^login/$', views.login_view, name='login'),
    re_path(r'^logout/$', views.logout_view, name='logout'),
]