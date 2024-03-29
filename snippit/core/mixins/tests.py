import simplejson

from django.test.client import Client
from account.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from django.utils import unittest
from django.conf import settings

# Test User username and password
TEST_USERNAME = 'test'
TEST_PASSWORD = 123456
TEST_EMAIL = 'test@test.com'


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

    def assertHttpNotFound(self, response):
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def assertHttpUnauthorized(self, response):
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def assertHttpMethodNotAllowed(self, response):
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def assertHttpConflict(self, response):
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


class CommonTestMixin(HttpStatusCodeMixin):
    """
    Common Test Mixin
    """
    username = TEST_USERNAME
    password = TEST_PASSWORD
    email = TEST_EMAIL
    c = Client()
    client_header = {}
    u = User.objects.none()
    token = None

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
        self.token = request_json.get('token')
        # set header
        self.client_header['HTTP_AUTHORIZATION'] = 'Token %s' % (
            request_json.get('token'))

    def token_logout(self):
        """
        Token Logout
        """
        self.token_login()
        url = reverse('token-logout')
        self.c.get(path=url, **self.client_header)


class RestApiScenarioMixin(CommonTestMixin):

    def _get_auth(self, **kwargs):
        header = {}
        if kwargs.get('auth', False):
            self.token_login()
            header = self.client_header
        return header

    def _get_method(self, **kwargs):
        method = self.c.get
        if kwargs.get('request'):
            method = kwargs.get('request')
        return method

    def _get_data(self, **kwargs):
        data = {}
        if kwargs.get('data'):
            data = kwargs.get('data')
        return data

    def assertInvalidObjectResource(self, url, **kwargs):
        header = self._get_auth(**kwargs)
        request = self._get_method(**kwargs)
        data = self._get_data(**kwargs)
        response = request(url, data=data, content_type='application/json',
                           **header)
        self.assertHttpNotFound(response)
        return response

    def assertListResource(self, url, queryset, **kwargs):
        limit = settings.REST_FRAMEWORK['PAGINATE_BY']
        header = self._get_auth(**kwargs)
        request = self._get_method(**kwargs)
        data = self._get_data(**kwargs)
        response = request(url, data=data, content_type='application/json',
                           **header)
        content = simplejson.loads(response.content)
        self.assertHttpOk(response)
        self.assertIsInstance(content, dict)
        self.assertIsInstance(content['results'], list)
        if not data:
            self.assertEquals(content['count'], queryset.count())
            self.assertGreaterEqual(len(content['results']),
                                    queryset[:limit].count())
        return content
