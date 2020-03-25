from django.contrib import admin
from django.urls import include, re_path, path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from kihivasok import views as kihivasok_views
from ors import views as ors_views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^accounts/', include('accounts.urls', namespace='accounts')),
    re_path(r'^articles/', include('articles.urls', namespace='articles')),
    re_path(r'^ors/', include('ors.urls', namespace='ors')),
    path('ors_keresese/', ors_views.ors_status, name='status'),
    path('orsi_gyujtemeny/', ors_views.ors_patrol_collection, name='patrol_collection'),
    re_path(r'^kihivasok/', include('kihivasok.urls', namespace='challenge')),
    path('rolunk/',views.about),
    path('',kihivasok_views.challenge_list, name='home')
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)