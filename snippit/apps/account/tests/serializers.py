# -*- coding: utf-8 -*-
from django.test import TestCase
from account.models import User
from account.serializers import UserDetailSerializer


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
        self.assertEquals(serializer.errors.keys(), ['username', 'email'])
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