# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import AutoSlugField
from django.utils.encoding import smart_unicode
from django.conf import settings


class Tags(models.Model):
    """
    Snippet Tags
    """
    name = models.CharField(_('name'), max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')
        db_table = 'tags'

    def __unicode__(self):
        return smart_unicode('<%s (%s)>' % (self.name, self.id))


class Languages(models.Model):
    """
    Programming languages
    """
    name = models.CharField(_('name'), max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)

    class Meta:
        verbose_name = _('language')
        verbose_name_plural = _('languages')
        db_table = 'languages'

    def __unicode__(self):
        return smart_unicode('<%s (%s)>' % (self.name, self.id))


class Snippets(models.Model):
    """
    Code Snippets
    """
    name = models.CharField(_('snippet name'), max_length=255)
    description = models.TextField(_('description'), null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    is_public = models.BooleanField(default=True, db_index=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    created_at = models.DateTimeField(_('date joined'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated date'), auto_now=True)
    tags = models.ManyToManyField(Tags)

    class Meta:
        verbose_name = _('snippet')
        verbose_name_plural = _('snippets')
        db_table = 'snippets'

    def __unicode__(self):
        return smart_unicode('<%s (%s)>' % (self.name, self.id))


class Pages(models.Model):
    """
    Snippet Pages
    """
    content = models.TextField()
    snippet = models.ForeignKey(Snippets)
    language = models.ForeignKey(Languages)

    class Meta:
        verbose_name = _('page')
        verbose_name_plural = _('pages')
        db_table = 'snippets_pages'

    def __unicode__(self):
        return smart_unicode(
            '<%s - %s (%s)>' % (self.snippet.name, self.language.name,
                                self.id))


class Comments(models.Model):
    """
    Snippet Comments
    """
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    comment = models.TextField()
    snippet = models.ForeignKey(Snippets)
    created_at = models.DateTimeField(_('date joined'), auto_now_add=True)
    create_ip = models.IPAddressField()

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        db_table = 'snippets_comments'

    def __unicode__(self):
        return smart_unicode(
            '<%s - %s (%s)>' % (self.author.username, self.snippet.name,
                                self.id))
