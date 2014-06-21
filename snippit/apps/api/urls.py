from django.conf.urls import patterns, url, include
from auth.urls import api_urlpatterns

urlpatterns = patterns(
    '',
    url(r'^auth/', include(api_urlpatterns)),
)