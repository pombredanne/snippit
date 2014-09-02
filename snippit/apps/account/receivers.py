from django.dispatch import receiver
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from account.models import User
from .signals import welcome_email


@receiver(welcome_email, dispatch_uid="account.receivers.send_welcome_email")
def send_welcome_email(sender, user, **kwargs):
    """
    Welcome mail send for created user
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
