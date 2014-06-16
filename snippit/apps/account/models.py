# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.db import models
from .managers import UserManager
from snippet.models import Snippets


class User(AbstractBaseUser):
    """
    Users
    """
    username = models.CharField(_('username'), max_length=25, unique=True)
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
    website = models.CharField(_('Website'), max_length=65,
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
        return "%s(%s)" % (self.username, self.id)

    def get_full_name(self):
        return u"%s %s" % (self.first_name, self.last_name)


class Follow(models.Model):
    followee = models.ForeignKey(User, related_name='followee_set')
    follower = models.ForeignKey(User, related_name='follower_set')
    created_at = models.DateTimeField(_('Follow Created'), auto_now_add=True)

    object = models.Manager()

    class Meta:
        db_table = 'users_follow'

    def __unicode__(self):
        return '<%s> <%s> %s' % (self.follower.username,
                                 self.followee.username, self.created_at)