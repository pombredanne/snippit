from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode
from django.conf import settings


class Organization(models.Model):
    name = models.CharField(_('name'), max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)
    description = models.TextField(null=True, blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('organization')
        verbose_name_plural = _('organizations')
        db_table = 'organization'

    def __unicode__(self):
        return smart_unicode('<%s (%s)>' % (self.name, self.id))


class Member(models.Model):
    organization = models.ForeignKey(Organization, related_name='members')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    ADMIN = 2
    USER = 1
    PERMISSIONS = ((ADMIN, 'Admin'), (USER, 'User'),)

    rule = models.PositiveIntegerField(max_length=10, choices=PERMISSIONS)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name='member_approves',
                                    null=True, blank=True)

    class Meta:
        verbose_name = _('organization member')
        verbose_name_plural = _('organization members')
        db_table = 'organization_members'
        unique_together = ('organization', 'user',)

    def __unicode__(self):
        return smart_unicode('<%s member of (%s)>' % (self.organization.name,
                                                      self.user.username))
