# -*- coding: utf-8 -*-
import simplejson

from django.test import TestCase
from account.models import User
from snippit.core.mixins import CommonTestMixin, HttpStatusCodeMixin
from django.core.urlresolvers import reverse


class UserRegisterViewTest(CommonTestMixin, HttpStatusCodeMixin, TestCase):
    """
    UserRegisterView Test Cases
    """
    fixtures = ('initial_data', )

    def test_invalid_data(self):
        """
        invalid form data
        """
        url = reverse('register')
        user = User.objects.filter().order_by('?')[0]
        data = {'username': user.username, 'email': user.email,
                'password': '123456'}
        response = self.c.post(url, data=simplejson.dumps(data),
                               content_type='application/json')
        response_dict = simplejson.loads(response.content)
        self.assertHttpBadRequest(response)
        self.assertEquals(sorted(response_dict.keys()), ['email', 'username'])
        self.assertEquals(response_dict['username'],
                          ['User with this Username already exists.'])
        self.assertEquals(response_dict['email'],
                          ['User with this Email address already exists.'])

    def test_create_user(self):
        """
        valid form data
        """
        url = reverse('register')
        data = {'username': 'testviewuser', 'email': 'testviewuser@test.com',
                'password': '123456'}
        response = self.c.post(url, data=simplejson.dumps(data),
                               content_type='application/json')
        response_dict = simplejson.loads(response.content)
        self.assertHttpCreated(response)
        self.assertTrue(User.objects.filter(
            username=response_dict['username'],
            email=response_dict['email']).exists())

    def test_not_allowed_request(self):
        """
        UserRegisterView allowed method POST(create)
        """
        url = reverse('register')
        response = self.c.get(url)
        self.assertHttpMethodNotAllowed(response)


class UserDetailViewTest(CommonTestMixin, HttpStatusCodeMixin, TestCase):
    """
    User Detail or Update Test Cases
    """
    fixtures = ('initial_data', )

    def test_user_detail(self):
        """
        Check api User Detail response
        """
        user = User.objects.filter().order_by('?')[0]
        url = reverse('user-detail', kwargs={'username': user.username})
        response = self.c.get(url)
        content = simplejson.loads(response.content)
        self.assertHttpOk(response)
        self.assertEqual(content['username'], user.username)
        self.assertEqual(content['email'], user.email)
        self.assertEqual(content['followings'], user.followers.count())
        self.assertEqual(content['followers'], user.following.count())

    def test_user_update_used_email(self):
        """
        User Profile Update used email/username
        """
        user1 = User.objects.get(username=self.username, email=self.email)
        user2 = User.objects.filter().order_by('?')[0]
        url = reverse('user-detail', kwargs={'username': user1.username})
        data = {'username': user2.username, 'email': user2.email}
        self.token_login()
        response = self.c.put(url, simplejson.dumps(data),
                              content_type='application/json',
                              **self.client_header)
        content = simplejson.loads(response.content)
        self.assertHttpBadRequest(response)
        self.assertEquals(sorted(content.keys()), ['email', 'username'])
        self.assertEquals(content['username'],
                          ['User with this Username already exists.'])
        self.assertEquals(content['email'],
                          ['User with this Email address already exists.'])

    def test_user_update_required_fields_be_empty(self):
        """
        User Update Required Fields be empty
        """
        user = User.objects.get(username=self.username, email=self.email)
        url = reverse('user-detail', kwargs={'username': user.username})
        self.token_login()
        response = self.c.put(url, **self.client_header)
        content = simplejson.loads(response.content)
        self.assertHttpBadRequest(response)
        self.assertEquals(sorted(content.keys()), ['email', 'username'])
        self.assertEquals(content['username'], ['This field is required.'])
        self.assertEquals(content['email'], ['This field is required.'])

    def test_not_allowed_request(self):
        """
        Allowed method PUT(update)
        POST method data will be added. user already in use
        """
        user = User.objects.get(username=self.username, email=self.email)
        self.token_login()
        url = reverse('user-detail', kwargs={'username': user.username})
        response = self.c.post(url, **self.client_header)
        self.assertHttpMethodNotAllowed(response)

    def test_user_updated_not_authenticate(self):
        """
        update for authenticated user can be made
        """
        user = User.objects.get(username=self.username, email=self.email)
        url = reverse('user-detail', kwargs={'username': user.username})
        data = {'username': user.username, 'email': user.email,
                'first_name': 'test', 'last_name': 'test'}
        response = self.c.put(url, simplejson.dumps(data))
        self.assertHttpForbidden(response)

    def test_user_update(self):
        """
        Updating of user information
        """
        user = User.objects.get(username=self.username, email=self.email)
        self.token_login()
        url = reverse('user-detail', kwargs={'username': user.username})
        data = {'username': user.username, 'email': user.email,
                'first_name': 'test', 'last_name': 'test'}
        response = self.c.put(url, simplejson.dumps(data),
                              content_type='application/json',
                              **self.client_header)
        self.assertHttpOk(response)
        self.assertEquals(User.objects.get(id=user.id).first_name, 'test')
        self.assertEquals(User.objects.get(id=user.id).last_name, 'test')

    def test_update_other_user_information(self):
        """
        You don't have permission to update other users
        """
        user = User.objects.filter().order_by('?')[0]
        self.token_login()
        url = reverse('user-detail', kwargs={'username': user.username})
        data = {'username': user.username, 'email': user.email,
                'first_name': 'test', 'last_name': 'test'}
        response = self.c.put(url, simplejson.dumps(data),
                              content_type='application/json',
                              **self.client_header)
        self.assertHttpForbidden(response)