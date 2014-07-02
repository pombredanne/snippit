from django.conf.urls import patterns, url, include
from .views import (UserRegisterView, UserDetailView, UserFollowersView,
                    UserFollowingsView, UserStarredSnippetsView)

api_urlpatterns = patterns(
    '',
    url(r'^$', UserRegisterView.as_view(), name='register'),
    url(r'^(?P<username>[A-Za-z0-9-_]+)/$', UserDetailView.as_view(),
        name='user-detail'),
    url(r'^(?P<username>[A-Za-z0-9-_]+)/', include(patterns(
        '',
        url(r'^followers/$', UserFollowersView.as_view(),
            name='user-followers'),
        url(r'^followings/$', UserFollowingsView.as_view(),
            name='user-followings'),
        url(r'^stars/$', UserStarredSnippetsView.as_view(), name='user-stars'),
    )))
)