import simplejson

from datetime import datetime
from django.test import TestCase
from django.core.urlresolvers import reverse
from snippit.core.mixins import CommonTestMixin, HttpStatusCodeMixin
from rest_framework.authtoken.models import Token


class SessionAuthenticationTest(CommonTestMixin, HttpStatusCodeMixin, TestCase):
    """
    Session Authentication Test Cases (Basic Authentication)
    """
    fixtures = ('test_accounts', )

    def test_session_login(self):
        """
        Session Login
        """
        url = reverse('session-login')
        payload = simplejson.dumps({'username': self.username,
                                    'password': self.password})
        response = self.c.post(path=url, data=payload,
                               content_type='application/json')
        self.assertHttpOk(response)

    def test_session_invalid_user_login(self):
        """
        user name or password is invalid
        """
        url = reverse('session-login')
        payload = simplejson.dumps({'username': 'invalid',
                                    'password': 'invalid'})
        response = self.c.post(path=url, data=payload,
                               content_type='application/json')
        self.assertHttpBadRequest(response)

    def test_session_logout(self):
        """
        Session Logout
        """
        url = reverse('session-logout')
        # session login
        self.session_login()
        response = self.c.post(path=url, content_type='application/json')
        self.assertHttpOk(response)

    def test_session_logout_not_authenticated(self):
        """
        Authentication must be required.
        The output of authenticated user should be made
        """
        url = reverse('session-logout')
        response = self.c.post(path=url, content_type='application/json')
        self.assertHttpForbidden(response)


class TokenAuthenticationTest(CommonTestMixin, HttpStatusCodeMixin, TestCase):
    """
    Token Authentication Test Cases
    """

    def test_token_login(self):
        """
        Token Login
        """
        url = reverse('token-login')
        payload = simplejson.dumps({'username': self.username,
                                    'password': self.password})
        response = self.c.post(path=url, data=payload,
                               content_type='application/json')
        self.assertHttpOk(response)
        self.assertTrue(Token.objects.filter(user=self.u).exists())

    def test_token_invalid_user_login(self):
        """
        user name or password is invalid
        """
        date = datetime.now()
        url = reverse('token-login')
        payload = simplejson.dumps({'username': 'invalid',
                                    'password': 'invalid'})
        response = self.c.post(path=url, data=payload,
                               content_type='application/json')
        self.assertHttpBadRequest(response)
        self.assertFalse(Token.objects.filter(
            user=self.u, created__lt=date).exists())

    def test_token_logout(self):
        """
        Token Logout
        """
        # Token Login
        self.token_login()
        url = reverse('token-logout')
        response = self.c.post(path=url,  **self.client_header)
        self.assertHttpOk(response)
        self.assertFalse(Token.objects.filter(user=self.u).exists())

    def test_token_logout_not_authenticated(self):
        """
        Authentication must be required.
        The output of authenticated user should be made
        """
        date = datetime.now()
        url = reverse('token-logout')
        response = self.c.post(path=url, content_type='application/json')
        self.assertHttpForbidden(response)
        self.assertFalse(Token.objects.filter(
            user=self.u, created__lt=date).exists())
