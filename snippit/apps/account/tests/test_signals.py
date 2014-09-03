# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core import mail
from account.models import User, Follow
from snippet.models import Snippets
from snippit.core.mixins import CommonTestMixin
from snippit.core.signals import mock_signal_receiver
from account.signals import welcome_email, follow_done


class WelcomeEmailSignalTestCase(CommonTestMixin, TestCase):
    """
    Welcome email signal test for created user
    """

    def test_welcome_email(self):
        user = User.objects.filter().order_by('?')[0]
        with mock_signal_receiver(welcome_email) as receiver:
            welcome_email.send(sender=self, user=user)
            self.assertEqual(receiver.call_count, 1)
            send_mail = mail.outbox[0]
            self.assertEqual(len(mail.outbox), 1)
            expected_to = [user.email]
            self.assertEqual(expected_to, send_mail.to)

    def test_incorrect_object(self):
        snippet = Snippets.objects.filter().order_by('?')[0]
        self.assertRaises(AssertionError, welcome_email.send,
                          sender=self, user=snippet)


class FollowNotificationSignalTestCase(CommonTestMixin, TestCase):
    """
    Follow Notification Test Cases
    """

    def test_follow_notification(self):
        follow = Follow.objects.filter().order_by('?')[0]
        with mock_signal_receiver(follow_done) as receiver:
            follow_done.send(sender=self, follow=follow)
            self.assertEqual(receiver.call_count, 1)
            self.assertEqual(len(mail.outbox), 1)
            send_mail = mail.outbox[0]
            expected_to = [follow.following.email]
            self.assertEqual(expected_to, send_mail.to)

    def test_incorrect_object(self):
        snippet = Snippets.objects.filter().order_by('?')[0]
        self.assertRaises(AssertionError, follow_done.send,
                          sender=self, follow=snippet)
