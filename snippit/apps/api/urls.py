from django.conf.urls import patterns, url, include
from auth.urls import api_urlpatterns as auth_urls
from account.urls import api_urlpatterns as account_urls

urlpatterns = patterns(
    '',
    url(r'^auth/', include(auth_urls)),
    url(r'^account/', include(account_urls)),
)