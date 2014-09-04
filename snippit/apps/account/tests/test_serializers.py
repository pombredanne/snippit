# -*- coding: utf-8 -*-
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from account.models import User, Follow
from account.serializers import (UserDetailSerializer, UserRegisterSerializer,
                                 UserFollowSerializer,
                                 UserChangePasswordSerializer)

factory = APIRequestFactory()
# Just to ensure we have a request in the serializer context
request = factory.get('/')


class UserDetailSerializerTestCase(TestCase):
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

    def test_check_unique_fields(self):
        """
        changed email/username used
        """
        user1 = User.objects.filter().order_by('?')[0]
        user2 = User.objects.filter().order_by('?')[0]
        serializer = UserDetailSerializer(instance=user1, data={
            'username': user2.username, 'email': user2.email})
        self.assertFalse(serializer.is_valid())
        self.assertEquals(sorted(serializer.errors.keys()),
                          ['email', 'username'])
        self.assertEquals(serializer.errors['username'],
                          ['User with this Username already exists.'])
        self.assertEquals(serializer.errors['email'],
                          ['User with this Email address already exists.'])


class UserRegisterSerializerTestCase(TestCase):
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
                          ['User with this Username already exists.'])
        self.assertEquals(serializer.errors['email'],
                          ['User with this Email address already exists.'])

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


class UserFollowSerializerTestCase(TestCase):
    """
    UserFollowSerializer Test Cases
    """
    fixtures = ('initial_data', )

    def test_valid_serializer(self):
        """
        valid parameters
        """
        follow = Follow.objects.filter()[0]
        serializer = UserFollowSerializer(instance=follow)
        self.assertTrue(sorted(serializer.data.keys()),
                        ['follower', 'following'])
        self.assertIsInstance(serializer.data['follower'], dict)
        self.assertIsInstance(serializer.data['following'], dict)


class UserChangePasswordSerializerTestCase(TestCase):
    """
    UserChangePasswordSerializer Test Cases
    """
    fixtures = ('initial_data', )

    def test_valid_serializer(self):
        user = User.objects.filter().order_by('?')[0]
        user.set_password('123456')
        user.save()
        data = {'password': '123456', 'new_password': '12345',
                'confirm_password': '12345'}
        serializer = UserChangePasswordSerializer(data=data, instance=user,
                                                  context={'request': request})
        self.assertTrue(serializer.is_valid())
        serializer.save(force_update=True)
        self.assertTrue(user.check_password('12345'))

    def test_invalid_password(self):
        user = User.objects.filter().order_by('?')[0]
        data = {'password': 'testdd', 'new_password': '12345',
                'confirm_password': '12345'}
        serializer = UserChangePasswordSerializer(data=data, instance=user,
                                                  context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEquals(len(serializer.errors), 1)
        self.assertEquals(serializer.errors.keys(), ['password'])
        self.assertEquals(serializer.errors['password'], [u'passwords invalid'])

    def test_not_match_passwords(self):
        user = User.objects.filter().order_by('?')[0]
        user.set_password('123456')
        user.save()
        data = {'password': '123456', 'new_password': '1234',
                'confirm_password': '12345'}
        serializer = UserChangePasswordSerializer(data=data, instance=user,
                                                  context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEquals(len(serializer.errors), 1)
        self.assertEquals(serializer.errors.keys(), ['non_field_errors'])
        self.assertEquals(serializer.errors['non_field_errors'],
                          [u'passwords did not match'])
