from django.core.mail import send_mail
from django.dispatch import receiver
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from .signals import snippet_add_comment
from snippet.models import Snippets, Comments


@receiver(snippet_add_comment,
          dispatch_uid="snippet.receivers.send_add_comment_email")
def send_add_comment_email(sender, snippet, comment, **kwargs):
    """
    Send the email notification After writing reviews in snippet

    :param sender: Signal Sender Class
    :param snippet: commented snippet
    :param comment: recent comment
    >>> snippet_add_comment.send(sender=self, snippet=snippet, comment=comment)
    """
    # check
    assert isinstance(snippet, Snippets)
    assert isinstance(comment, Comments)

    notification = settings.MAIL_NOTIFICATION.get('add_comment')
    data = Context({'snippet': snippet, 'comment': comment})
    template = get_template(notification['template'])
    message = template.render(data)
    # comment senders
    mails = list(snippet.comments_set.exclude(
        author__id=comment.author.id).values_list('author__email', flat=True))
    if comment.author != snippet.created_by:
        mails.append(snippet.created_by.email)
    # subscribers
    mails.extend(snippet.subscribers.values_list('email', flat=True))
    # unique mail list
    mails = set(mails)
    send_mail(notification['subject'], message,
              settings.NOTIFICATION_FROM_EMAIL, mails)
