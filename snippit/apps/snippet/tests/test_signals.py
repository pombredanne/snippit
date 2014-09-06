# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core import mail
from snippet.models import Comments
from snippit.core.mixins import CommonTestMixin
from snippit.core.signals import mock_signal_receiver
from snippet.signals import snippet_add_comment


class AddCommentNotificationSignalTestCase(CommonTestMixin, TestCase):
    """
    Send the email notification After writing reviews in snippet test cases
    """
    fixtures = ('initial_data', )

    def test_add_comment_signal(self):
        comment = Comments.objects.filter().order_by('?')[0]
        with mock_signal_receiver(snippet_add_comment) as receiver:
            snippet_add_comment.send(sender=self, snippet=comment.snippet,
                                     comment=comment)
            self.assertEqual(receiver.call_count, 1)
            self.assertGreater(mail.outbox, 0)
