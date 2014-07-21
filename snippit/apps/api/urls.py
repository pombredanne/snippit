from django.conf.urls import patterns, url, include
from auth.urls import auth_urls
from account.urls import account_urls
from snippet.urls import tags_urls, languages_urls, snippets_urls

urlpatterns = patterns(
    '',
    url(r'^auth/', include(auth_urls)),
    url(r'^account/', include(account_urls)),
    url(r'^languages/', include(languages_urls)),
    url(r'^tags/', include(tags_urls)),
    url(r'^snippets/', include(snippets_urls)),
)
