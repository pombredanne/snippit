from django.conf.urls import patterns, url
from .views import (SessionLogoutView, SessionAuthenticationView,
                    TokenLogoutView)
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = patterns(
    '',
    url(r'^login/$', SessionAuthenticationView.as_view(), name='session-login'),
    url(r'^logout/$', SessionLogoutView.as_view(), name='session-logout')
)


api_urlpatterns = patterns(
    '',
    url(r'^login/$', ObtainAuthToken.as_view(), name='token-login'),
    url(r'^logout/$', TokenLogoutView.as_view(), name='token-logout')
)