# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractBaseUser
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils.encoding import smart_unicode
from django.dispatch import receiver
from .managers import UserManager
from snippet.models import Snippets
from .validators import validate_username
from django.conf import settings
from django.template.loader import get_template
from django.template import Context
from .signals import welcome_email, follow_done


class User(AbstractBaseUser):
    """
    Users
    """
    username = models.CharField(_('username'), max_length=30, unique=True,
                                validators=[validate_username])
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(_('is active'), default=True)
    first_name = models.CharField(_('first name'), max_length=255,
                                  null=True, blank=True)
    last_name = models.CharField(_('last name'), max_length=255,
                                 null=True, blank=True)
    recovery_key = models.CharField(_('Recovery Key'), max_length=255,
                                    null=True, blank=True)
    location = models.CharField(_('Location'), max_length=65,
                                null=True, blank=True)
    website = models.URLField(_('Website'), max_length=65,
                              null=True, blank=True)
    created_at = models.DateTimeField(_('date joined'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated date'), auto_now=True)
    stars = models.ManyToManyField(Snippets)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'users'

    def __unicode__(self):
        return smart_unicode("%s(%s)" % (self.username, self.id))

    def email_user(self, subject, message, from_email=None):
        from_email = from_email if from_email else settings.NOTIFICATION_FROM_EMAIL
        send_mail(subject, message, from_email, [self.email])

    def get_full_name(self):
        return smart_unicode("%s %s" % (self.first_name, self.last_name))

    def get_followers(self):
        followers = self.followers.all().values_list('follower__id', flat=True)
        return User.objects.filter(id__in=followers)

    def get_followings(self):
        followers = self.following.all().values_list('following__id', flat=True)
        return User.objects.filter(id__in=followers, is_active=True)


class Follow(models.Model):
    """
    A relationship model for following users
    """
    follower = models.ForeignKey(User, related_name="following")
    following = models.ForeignKey(User, related_name="followers")

    def __unicode__(self):
        return smart_unicode("%s following %s" % (self.follower.username,
                                                  self.following.username))

    class Meta:
        unique_together = (('follower', 'following', ))


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
def send_follow_email(sender, follow, **kwargs):
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
