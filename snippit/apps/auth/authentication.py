import datetime

from django.utils.timezone import utc
from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from django.conf import settings


class ExpiringTokenAuthentication(TokenAuthentication):
    """
    Token Authentication Backend
    """

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted')

        utc_now = datetime.datetime.utcnow().replace(tzinfo=utc)

        # do not check for this in Token Authentication
        if token.created < utc_now - datetime.timedelta(
                days=settings.API_TOKEN_TTL):
            raise exceptions.AuthenticationFailed('Token has expired')

        return token.user, token