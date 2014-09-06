from django.conf.urls import patterns, url
from snippet import views

languages_urls = patterns(
    '',
    url(r'^$', views.LanguagesView.as_view(), name='languages-list'),
    url(r'^(?P<slug>[A-Za-z0-9-_]+)/snippets/$',
        views.LanguageSnippetsView.as_view(), name='language-snippets-list'),
)

tags_urls = patterns(
    '',
    url(r'^$', views.TagsView.as_view(), name='tags-list'),
    url(r'^(?P<slug>[A-Za-z0-9-_]+)/snippets/$',
        views.TagSnippetsViews.as_view(), name='tag-snippets-list'),
)

snippets_urls = patterns(
    '',
    url(r'^$', views.SnippetsView.as_view(), name='snippets-list'),
    url(r'^(?P<slug>[A-Za-z0-9-_]+)/$',
        views.SnippetDetailView.as_view(), name='snippets-detail'),
    url(r'^(?P<slug>[A-Za-z0-9-_]+)/comments/$',
        views.SnippetCommentsView.as_view(), name='snippets-comments'),
    url(r'^(?P<slug>[A-Za-z0-9-_]+)/star/$',
        views.SnippetStarView.as_view(), name='snippets-star'),
    url(r'^(?P<slug>[A-Za-z0-9-_]+)/star/users/$',
        views.SnippetStarredUsersView.as_view(), name='snippets-starred-users'),
    url(r'^(?P<slug>[A-Za-z0-9-_]+)/subscribers/$',
        views.SnippetSubscribersView.as_view(), name='snippets-subscribers'),
)
