from django.conf.urls import patterns, url
from .views import (SessionLogoutView, SessionAuthenticationView,
                    TokenLogoutView, TokenAuthenticationView)

urlpatterns = patterns(
    '',
    url(r'^login/$', SessionAuthenticationView.as_view(), name='session-login'),
    url(r'^logout/$', SessionLogoutView.as_view(), name='session-logout')
)


auth_urls = patterns(
    '',
    url(r'^login/$', TokenAuthenticationView.as_view(), name='token-login'),
    url(r'^logout/$', TokenLogoutView.as_view(), name='token-logout')
)