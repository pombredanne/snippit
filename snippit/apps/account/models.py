# -*- coding: utf-8 -*-
import re
import requests
import simplejson

from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.db import transaction
from django.core import validators
from django.utils.encoding import smart_unicode
from .managers import UserManager
from snippet.models import Snippets


class User(AbstractBaseUser):
    """
    Users
    """
    username = models.CharField(_('username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                    '@/./+/-/_ characters'),
        validators=[
            validators.RegexValidator(re.compile('^[\w.@+-]+$'),
                                      _('Enter a valid username.'), 'invalid')
        ])
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

    def get_full_name(self):
        return smart_unicode("%s %s" % (self.first_name, self.last_name))

    @staticmethod
    def dummy_user(quantity, password):
        """
        create dummy user
        """
        with transaction.atomic():
            assert quantity > 0
            r = requests.get('http://api.randomuser.me/?results=%s' % quantity)
            assert r.status_code == 200
            contents = simplejson.loads(r.content)
            assert isinstance(contents, dict)
            assert 'results' in contents
            users = []
            for content in contents['results']:
                user = content['user']
                if User.objects.filter(username=user['username']).exists():
                    continue
                u = User.objects.create_user(username=user['username'],
                                             password=password,
                                             email=user['email'],
                                             first_name=user['name']['first'],
                                             last_name=user['name']['last'])
                users.append(u)
        return users


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name="following")
    following = models.ForeignKey(User, related_name="followers")

    def __unicode__(self):
        return smart_unicode("%s following %s" % (self.follower.username,
                                                  self.following.username))