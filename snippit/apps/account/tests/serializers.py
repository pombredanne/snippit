# -*- coding: utf-8 -*-
from django.test import TestCase
from account.models import User
from account.serializers import UserDetailSerializer, UserRegisterSerializer


class UserDetailSerializerTests(TestCase):
    """
    UserDetailSerializer Test Cases
    """
    fixtures = ('initial_data', )

    def test_check_required_fields(self):
        """
        check required fields
        """
        serializer = UserDetailSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEquals(sorted(serializer.errors.keys()),
                          ['email', 'username'])
        self.assertEquals(serializer.errors['username'],
                          [u'This field is required.'])
        self.assertEquals(serializer.errors['email'],
                          [u'This field is required.'])

    def test_check_read_only_fields(self):
        """
        Check read only fields
        """
        serializer = UserDetailSerializer(data={
            'username': 'test', 'email': 'test@test.com', 'followings': 10,
            'created_at': '2014-10-1-0 12:12', 'followers': 10})
        self.assertTrue(serializer.is_valid())
        self.assertNotIn(serializer.data.keys(),
                         ['created_at', 'followings', 'followers'])

    def test_check_data(self):
        """
        Check Serializer data
        """
        user = User.objects.filter(following__gt=0).order_by('?')[0]
        serializer = UserDetailSerializer(instance=user)
        data = serializer.data
        self.assertEqual(data['username'], user.username)
        self.assertEqual(data['email'], user.email)
        self.assertEqual(data['followings'], user.followers.count())
        self.assertEqual(data['followers'], user.following.count())


class UserRegisterSerializerTest(TestCase):
    """
    UserRegisterSerializer Test Cases
    """
    fixtures = ('initial_data', )

    def test_check_required_fields(self):
        """
        check required fields
        """
        serializer = UserRegisterSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertEquals(sorted(serializer.errors.keys()),
                          ['email', 'password', 'username'])
        self.assertEquals(serializer.errors['username'],
                          [u'This field is required.'])
        self.assertEquals(serializer.errors['email'],
                          [u'This field is required.'])
        self.assertEquals(serializer.errors['password'],
                          [u'This field is required.'])

    def test_check_unique_fields(self):
        """
        Username, email must be unique
        """
        user = User.objects.filter().order_by('?')[0]
        data = {'username': user.username, 'email': user.email,
                'password': '123456'}
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(sorted(serializer.errors.keys()),
                          ['email', 'username'])
        self.assertEquals(serializer.errors['username'],
                          [u'username this already exists'])
        self.assertEquals(serializer.errors['email'],
                          [u'E-Mail this already exists'])

    def test_invalid_username(self):
        """
        Username regex: [A-Za-z0-9-_]{4,25}
        """
        data = {'username': 'aaa', 'email': 'testserializer@test.com',
                'password': '123456'}
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(serializer.errors.keys(), ['username'])
        self.assertEquals(serializer.errors['username'], [u'invalid username'])

    def test_invalid_email(self):
        """
        check email field
        """
        data = {'username': 'testusers', 'email': 'testserial@test',
                'password': '123456'}
        serializer = UserRegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEquals(serializer.errors.keys(), ['email'])
        self.assertEquals(serializer.errors['email'],
                          [u'Enter a valid email address.'])

    def test_valid_serializer(self):
        """
        valid parameters
        """
        data = {'username': 'testusers', 'email': 'testserial@test.com',
                'password': '123456'}
        serializer = UserRegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
