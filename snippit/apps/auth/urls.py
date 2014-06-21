from django.conf.urls import patterns, url
from .views import (SessionLogoutView, SessionAuthenticationView,
                    TokenLogoutView)
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = patterns(
    '',
    url(r'^login/$', SessionAuthenticationView.as_view(), name='login'),
    url(r'^logout/$', SessionLogoutView.as_view(), name='logout')
)


api_urlpatterns = patterns(
    '',
    url(r'^login/$', ObtainAuthToken.as_view()),
    url(r'^logout/$', TokenLogoutView.as_view())
)