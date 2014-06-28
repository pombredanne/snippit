from django.conf.urls import patterns, url
from .views import UserRegisterView

api_urlpatterns = patterns(
    '',
    url(r'^$', UserRegisterView.as_view(), name='register'),
)