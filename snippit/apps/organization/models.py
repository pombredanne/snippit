from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode
from account.models import User


class Organization(models.Model):
    name = models.CharField(_('name'), max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)
    description = models.TextField(null=True, blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.BooleanField(auto_created=True)
    created_by = models.ForeignKey(User)

    class Meta:
        verbose_name = _('organization')
        verbose_name_plural = _('organizations')
        db_table = 'organization'

    def __unicode__(self):
        return smart_unicode('<%s (%s)>' % (self.name, self.id))


class Member(models.Model):
    organization = models.ForeignKey(Organization, related_name='members')
    user = models.ForeignKey(User)

    ADMIN = 1
    USER = 1
    PERMISSIONS = ((ADMIN, 'Admin'), (User, 'User'),)

    rule = models.PositiveIntegerField(max_length=10, choices=PERMISSIONS)
    is_approved = models.BooleanField()
    created_at = models.BooleanField(auto_created=True)

    class Meta:
        verbose_name = _('organization member')
        verbose_name_plural = _('organization members')
        db_table = 'organization_members'

    def __unicode__(self):
        return smart_unicode('<%s member of (%s)>' % (self.organization.name,
                                                      self.user.username))
