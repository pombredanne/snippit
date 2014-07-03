# -*- coding: utf-8 -*-
from django.test import TestCase
from account.models import User
from snippet.models import Snippets
from snippet.serializers import SlimSnippetsSerializer


class SlimSnippetsSerializerTests(TestCase):
    """
    SlimSnippetsSerializer Test Cases
    """
    fixtures = ('initial_data', )

    def test_valid_serializer(self):
        """
        valid parameters
        """
        user = User.objects.filter().order_by('?')[0]
        snippet = Snippets.objects.exclude(user__id=user.id).order_by('?')[0]
        user.stars.add(snippet)
        serializer = SlimSnippetsSerializer(instance=user.stars.all(),
                                            many=True)
        self.assertIsInstance(serializer.data, list)
        self.assertEquals(len(serializer.data), user.stars.count())

    def test_snippet_stars(self):
        """
        Check snippet stars count
        """
        user = User.objects.filter().order_by('?')[0]
        snippet = Snippets.objects.exclude(user__id=user.id).order_by('?')[0]
        user.stars.add(snippet)
        serializer = SlimSnippetsSerializer(instance=snippet)
        self.assertEquals(serializer.data['stars'], snippet.user_set.count())