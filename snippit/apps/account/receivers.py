from django.dispatch import receiver
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from account.models import User, Follow
from .signals import welcome_email, follow_done


@receiver(welcome_email, dispatch_uid="account.receivers.send_welcome_email")
def send_welcome_email(sender, user, **kwargs):
    """
    Welcome mail send for created user

    :param sender: Signal Sender Class
    :param user: created user
    >>> welcome_email.send(sender=self, user=user)
    """
    # check
    assert isinstance(user, User)

    notification = settings.MAIL_NOTIFICATION.get('welcome_email')
    data = Context({'user': user})
    template = get_template(notification['template'])
    # generate mail template
    message = template.render(data)
    # send mail
    user.email_user(subject=notification['subject'] % user.username,
                    message=message)


@receiver(follow_done, dispatch_uid="account.receivers.send_follow_email")
def send_follow_email(selder, follow, **kwargs):
    """
    Follow mail send for following user

    :param sender: Signal Sender Class
    :param user: following
    >>> follow_done.send(sender=self, user=user)
    """
    # check
    assert isinstance(follow, Follow)

    notification = settings.MAIL_NOTIFICATION.get('follow')
    data = Context({'following': follow.following, 'follower': follow.follower})
    template = get_template(notification['template'])
    # generate mail template
    message = template.render(data)
    # send mail
    follow.following.email_user(
        subject=notification['subject'] % follow.following.username,
        message=message)
