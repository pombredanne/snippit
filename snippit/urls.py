from django.conf.urls import patterns, url, include
from django.views.generic.base import TemplateView

# custom signals
from account.receivers import send_welcome_email, follow_done
from snippet.receivers import send_add_comment_email

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='layout.html'),
        name='layout'),
    url(r'^auth/', include('auth.urls')),
    url(r'^api/', include('api.urls')),
)
