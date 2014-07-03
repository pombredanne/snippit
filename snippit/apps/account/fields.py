import urllib
import hashlib

from rest_framework.fields import Field
from django.conf import settings


class GravatarField(Field):
    """
    Email to Gravatar Url
    """

    def field_to_native(self, obj, field_name):
        source = self.source if self.source else field_name
        email = getattr(obj, source, '')
        email_hash = hashlib.md5(email.lower().encode('utf8'))
        params = urllib.urlencode({
            'd': settings.GRAVATAR['default_avatar'],
            's': settings.GRAVATAR['size']
        })
        return self.to_native('%(base_url)s%(hash)s?%(params)s' % {
            'base_url': settings.GRAVATAR['base_url'],
            'hash': email_hash.hexdigest(),
            'params': params,
        })