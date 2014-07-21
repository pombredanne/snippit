from django.conf.urls import patterns, url, include
from account import views

account_urls = patterns(
    '',
    url(r'^$', views.UserRegisterView.as_view(), name='register'),
    url(r'^(?P<username>[A-Za-z0-9-_]+)/$', views.UserDetailView.as_view(),
        name='user-detail'),
    url(r'^(?P<username>[A-Za-z0-9-_]+)/', include(patterns(
        '',
        url(r'^followers/$', views.UserFollowersView.as_view(),
            name='user-followers'),
        url(r'^followings/$', views.UserFollowingsView.as_view(),
            name='user-followings'),
        url(r'^snippets/$', views.UserSnippetsView.as_view(),
            name='user-snippets'),
        url(r'^stars/$', views.UserStarredSnippetsView.as_view(),
            name='user-stars'),
    )))
)
