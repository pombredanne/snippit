from django.conf.urls import patterns, url
from snippet.views import SnippetDetailView, SnippetCommentsView, SnippetStarView
from .views import (LanguagesView, TagsView, LanguageSnippetsView,
                    TagSnippetsViews)

languages_urls = patterns(
    '',
    url(r'^$', LanguagesView.as_view(), name='languages-list'),
    url(r'^(?P<slug>[A-Za-z0-9-_]+)/snippets/$', LanguageSnippetsView.as_view(),
        name='language-snippets-list'),
)

tags_urls = patterns(
    '',
    url(r'^$', TagsView.as_view(), name='tags-list'),
    url(r'^(?P<slug>[A-Za-z0-9-_]+)/snippets/$', TagSnippetsViews.as_view(),
        name='tag-snippets-list'),
)

snippets_urls = patterns(
    '',
    url(r'^(?P<slug>[A-Za-z0-9-_]+)/$',
        SnippetDetailView.as_view(), name='snippets-detail'),
    url(r'^(?P<slug>[A-Za-z0-9-_]+)/comments/$',
        SnippetCommentsView.as_view(), name='snippets-comments'),
    url(r'^(?P<slug>[A-Za-z0-9-_]+)/star/$',
        SnippetStarView.as_view(), name='snippets-star'),
)
