# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractBaseUser
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils.encoding import smart_unicode
from .managers import UserManager
from snippet.models import Snippets
from .validators import validate_username
from django.conf import settings


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


from .receivers import follow_done, send_welcome_email
