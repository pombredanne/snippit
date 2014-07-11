from django.conf.urls import patterns, url
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
