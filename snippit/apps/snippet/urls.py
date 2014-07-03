from django.conf.urls import patterns, url
from .views import LanguagesView, TagsView

languages_urls = patterns(
    '',
    url(r'^$', LanguagesView.as_view(), name='languages-list'),
)

tags_urls = patterns(
    '',
    url(r'^$', TagsView.as_view(), name='tags-list'),
)
