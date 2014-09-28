# -*- coding: utf-8 -*-
from django.db.utils import IntegrityError
from django.test import TestCase
from account.models import User, Follow
from snippet.models import Snippet


class UserTestCase(TestCase):
    """
    User model test cases
    """

    fixtures = ('initial_data', )
    user_email = 'test@localhost.com'
    user_username = 'test'
    user_password = '123456'

    def test_user_creation(self):
        """
        Create user
        """
        u = User(username=self.user_username, email=self.user_email)
        u.set_password(self.user_password)
        u.save()
        self.assertIsNotNone(u.id)
        self.assertTrue(User.objects.filter(
            username=self.user_username).exists())
        self.assertEqual(User.objects.get(
            username=self.user_username).email, self.user_email)
        self.assertTrue(User.objects.get(username=self.user_username).is_active)
        self.assertIsNotNone(User.objects.get(
            username=self.user_username).created_at)

    def test_empty_username_with_manager(self):
        """
        User entries for the username required
        """
        self.assertRaises(ValueError,
                          User.objects.create_user, email=self.user_email,
                          password=self.user_password, username='')

    def test_unique_username_with_manager(self):
        """
        User entries for the username must be unique
        """
        user = User.objects.filter().order_by('?')[0]
        self.assertRaisesMessage(IntegrityError,
                                 'column username is not unique',
                                 User.objects.create_user,
                                 email=self.user_email,
                                 password=self.user_password,
                                 username=user.username)

    def test_user_creation_with_manager(self):
        """
        Create User with UserManager
        """
        u = User.objects.create_user(username=self.user_username,
                                     email=self.user_email,
                                     password=self.user_password)
        self.assertIsNotNone(u.id)
        self.assertTrue(User.objects.filter(
            username=self.user_username).exists())
        self.assertEqual(User.objects.get(
            username=self.user_username).email, self.user_email)
        self.assertEqual(User.objects.get(
            username=self.user_username).password, u.password)

    def test_user_delete(self):
        """
        Delete User
        """
        user = User.objects.filter().order_by('?')[0]
        user.delete()
        self.assertFalse(User.objects.filter(username=user.username).exists())

    def test_user_update(self):
        """
        Update User
        """
        user = User.objects.filter().order_by('?')[0]
        updated_at = user.updated_at
        user.first_name = 'test'
        user.save()
        self.assertEqual(User.objects.get(
            username=user.username).first_name, user.first_name)
        self.assertNotEqual(User.objects.get(
            username=user.username).updated_at, updated_at)

    def test_star_snippet(self):
        """
        Star Code Snippet
        """
        snippet = Snippet.objects.filter().order_by('?')[0]
        user = User.objects.exclude(snippet__in=(snippet, )).order_by('?')[0]
        user.stars.add(snippet)
        self.assertTrue(User.objects.get(id=user.id).stars.exists())
        self.assertEqual(User.objects.get(
            id=user.id).stars.get().id, snippet.id)


class FollowTestCase(TestCase):
    """
    Follow model test cases
    """
    fixtures = ('initial_data', )

    def test_follow_create(self):
        """
        Create Follow
        """
        user_1 = User.objects.filter(
            followers__isnull=True, following__isnull=True).order_by('?')[0]
        user_2 = User.objects.filter(followers__isnull=True,
                                     following__isnull=True) \
            .exclude(username=user_1.username).order_by('?')[0]
        f = Follow.objects.create(following=user_1, follower=user_2)
        self.assertIsNotNone(f.id)
        self.assertTrue(Follow.objects.filter(following=user_1,
                                              follower=user_2).exists())
        self.assertTrue(user_1.followers.filter().exists())
        self.assertTrue(user_2.following.filter().exists())

    def test_follow_already_exists(self):
        """
        Check Unique row
        """
        f = Follow.objects.filter()[0]
        self.assertRaisesMessage(IntegrityError,
                                 'columns follower_id, following_id are'
                                 ' not unique',
                                 Follow.objects.create,
                                 follower=f.follower,
                                 following=f.following)

    def test_follow_delete(self):
        """
        Delete Follow
        """
        # initial data
        f = Follow.objects.filter().order_by('?')[0]
        f.delete()
        self.assertFalse(Follow.objects.filter(id=f.id).exists())