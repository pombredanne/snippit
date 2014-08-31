from django.dispatch import receiver
from django.template.loader import get_template
from django.template import Context
from .signals import welcome_email


@receiver(welcome_email, dispatch_uid="account.receivers.send_welcome_email")
def send_welcome_email(sender, user, **kwargs):
    """
    Welcome mail send for created user
    """
    data = Context({'user': user})
    template = get_template('mail/welcome.html')
    # generate mail template
    message = template.render(data)
    # send mail
    user.email_user(subject='Welcome %s' % user.username, message=message)
