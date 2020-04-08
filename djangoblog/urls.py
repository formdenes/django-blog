from django.contrib import admin
from django.urls import include, re_path, path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from kihivasok import views as kihivasok_views
import oauth2_provider.views as oauth2_views
from ors import views as ors_views
#imports for oauth2 authentication
from django.contrib.auth.models import User, Group
from django.contrib import admin
admin.autodiscover()

from rest_framework import generics, permissions, serializers

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

#define serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)

#create API views
class UserList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['groups']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


#OAuth2 provider endpoints
oauth2_endpoint_views = [
    path('authorize/', oauth2_views.AuthorizationView.as_view(), name='authorize'),
    path('token/', oauth2_views.TokenView.as_view(), name="token"),
    path('revoke-token/', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

if settings.DEBUG:
    #OAuth2 Application Management endpoints
    oauth2_endpoint_views += [
        path('applications/', oauth2_views.ApplicationList.as_view(), name="list"),
        path('applications/register/',
             oauth2_views.ApplicationRegistration.as_view(), name="register"),
        path('applications/<pk>/',
             oauth2_views.ApplicationDetail.as_view(), name="detail"),
        path('applications/<pk>/delete/',
             oauth2_views.ApplicationDelete.as_view(), name="delete"),
        path('applications/<pk>/update/',
             oauth2_views.ApplicationUpdate.as_view(), name="update"),
    ]

    # OAuth2 Token Management endpoints
    oauth2_endpoint_views += [
        path('authorized-tokens/', oauth2_views.AuthorizedTokensListView.as_view(),
             name="authorized-token-list"),
        path('authorized-tokens/<pk>/delete/', oauth2_views.AuthorizedTokenDeleteView.as_view(),
             name="authorized-token-delete"),
    ]

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^accounts/', include('accounts.urls', namespace='accounts')),
    re_path(r'^articles/', include('articles.urls', namespace='articles')),
    re_path(r'^ors/', include('ors.urls', namespace='ors')),
    path('ors_keresese/', ors_views.ors_status, name='status'),
    path('orsi_gyujtemeny/', ors_views.ors_patrol_collection, name='patrol_collection'),
    re_path(r'^kihivasok/', include('kihivasok.urls', namespace='challenge')),
    path('rolunk/',views.about),
    path('kereses/',kihivasok_views.kereses, name='search'),
    #OAuth2 endpoints:
    path('api/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('api/hello/', kihivasok_views.ProtectedEndPoint.as_view()),
    path('admin/users/', UserList.as_view()),
    path('admin/users/<pk>/', UserDetails.as_view()),
    path('admin/groups/', GroupList.as_view()),
    #default url
    path('',kihivasok_views.index, name='home')
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
