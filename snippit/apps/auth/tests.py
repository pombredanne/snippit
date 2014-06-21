import simplejson
from django.test import TestCase
from django.core.urlresolvers import reverse
from rest_framework import status
from snippit.core.mixins.tests import CommonTest


class SessionAuthenticationTest(CommonTest, TestCase):
    """
    Session Authentication (Basic Authentication)
    """
    fixtures = ('test_accounts', )

    def test_session_login(self):
        """
        Session Login
        """
        url = reverse('session-login')
        payload = simplejson.dumps({'username': self.username,
                                    'password': self.password})
        request = self.c.post(path=url, data=payload,
                              content_type='application/json')
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_session_invalid_user_login(self):
        """
        user name or password is invalid
        """
        url = reverse('session-login')
        payload = simplejson.dumps({'username': 'invalid',
                                    'password': 'invalid'})
        request = self.c.post(path=url, data=payload,
                              content_type='application/json')
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_session_logout(self):
        """
        Session Logout
        """
        url = reverse('session-logout')
        # session login
        self.session_login()
        request = self.c.post(path=url, content_type='application/json')
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_session_logout_not_authenticated(self):
        """
        Authentication must be required.
        The output of authenticated user should be made
        """
        url = reverse('session-logout')
        request = self.c.post(path=url, content_type='application/json')
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)


class TokenAuthenticationTest(CommonTest, TestCase):
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
        request = self.c.post(path=url, data=payload,
                              content_type='application/json')
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_token_invalid_user_login(self):
        """
        user name or password is invalid
        """
        url = reverse('token-login')
        payload = simplejson.dumps({'username': 'invalid',
                                    'password': 'invalid'})
        request = self.c.post(path=url, data=payload,
                              content_type='application/json')
        self.assertEqual(request.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_logout(self):
        """
        Token Logout
        """
        # Token Login
        self.token_login()
        url = reverse('token-logout')
        request = self.c.post(path=url,  **self.client_header)
        self.assertEqual(request.status_code, status.HTTP_200_OK)

    def test_token_logout_not_authenticated(self):
        """
        Authentication must be required.
        The output of authenticated user should be made
        """
        url = reverse('token-logout')
        request = self.c.post(path=url, content_type='application/json')
        self.assertEqual(request.status_code, status.HTTP_403_FORBIDDEN)