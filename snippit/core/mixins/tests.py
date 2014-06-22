import simplejson

from django.test.client import Client
from account.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from django.utils import unittest

# Test User username and password
TEST_USERNAME = 'test'
TEST_PASSWORD = 123456
TEST_EMAIL = 'test@test.com'


class CommonTestMixin(object):
    """
    Common Test Mixin
    """
    username = TEST_USERNAME
    password = TEST_PASSWORD
    email = TEST_EMAIL
    c = Client()
    client_header = {}
    u = User.objects.none()

    def setUp(self):
        """
        Dummy User
        """
        self.u = User.objects.create_user(username=self.username,
                                          password=self.password,
                                          email=self.email)

    def session_login(self, username=None, password=None):
        """
        Session Authentication
        """
        username = username if username else self.username
        password = password if password else self.password
        return self.c.login(username=username, password=password)

    def session_logout(self):
        """
        Session Logout
        """
        self.c.logout()

    def token_login(self, username=None, password=None):
        """
        Token Authentication
        """
        url = reverse('token-login')
        username = username if username else self.username
        password = password if password else self.password
        payload = simplejson.dumps({'username': username,
                                    'password': password})
        request = self.c.post(path=url, data=payload,
                              content_type='application/json')
        request_json = simplejson.loads(request.content)
        # set header
        self.client_header['HTTP_AUTHORIZATION'] = 'Token %s' % (
            request_json.get('token'))

    def token_logout(self):
        """
        Token Logout
        """
        self.token_login()
        url = reverse('token-logout')
        self.c.get(path=url,  **self.client_header)


class HttpStatusCodeMixin(unittest.TestCase):
    """
    HTTP Status Code Mixin
    """
    def assertHttpOk(self, response):
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def assertHttpCreated(self, response):
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def assertHttpNoContent(self, response):
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def assertHttpBadRequest(self, response):
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def assertHttpForbidden(self, response):
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)