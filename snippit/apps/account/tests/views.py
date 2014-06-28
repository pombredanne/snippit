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
                          [u'username this already exists'])
        self.assertEquals(response_dict['email'],
                          [u'E-Mail this already exists'])

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