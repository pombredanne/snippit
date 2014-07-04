# -*- coding: utf-8 -*-
from django.test import TestCase
from account.models import User
from snippet.models import Snippets, Tags, Languages
from snippet.serializers import (SlimSnippetsSerializer, TagsSerializer,
                                 LanguagesSerializer)


class SlimSnippetsSerializerTestCase(TestCase):
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
        self.assertTrue('stars' in serializer.data)
        self.assertEquals(serializer.data['stars'], snippet.user_set.count())

    def test_snippet_comments(self):
        """
        Check Snippet comments count
        """
        snippet = Snippets.objects.filter(comments__isnull=False)[0]
        serializer = SlimSnippetsSerializer(instance=snippet)
        self.assertTrue('comments' in serializer.data)
        self.assertEquals(serializer.data['comments'],
                          snippet.comments_set.count())


class TagsSerializerTestCase(TestCase):
    """
    TagsSerializer Test Cases
    """

    def test_valid_serializer(self):
        """
        valid parameters
        """
        tags = Tags.objects.all()[:15]
        serializer = TagsSerializer(instance=tags, many=True)
        self.assertIsInstance(serializer.data, list)
        self.assertEquals(len(serializer.data), tags.count())

    def test_snippets_count(self):
        """
        Check snippets count
        """
        tag = Tags.objects.filter(snippets__isnull=False).order_by('?')[0]
        serializer = TagsSerializer(instance=tag)
        self.assertIsInstance(serializer.data, dict)
        self.assertTrue('snippets' in serializer.data)
        self.assertEquals(serializer.data['snippets'], tag.snippets_set.count())

    def test_serializer_fields(self):
        """
        Check serializer Fields
        """
        tag = Tags.objects.filter(snippets__isnull=False).order_by('?')[0]
        serializer = TagsSerializer(instance=tag)
        self.assertIsInstance(serializer.data, dict)
        self.assertEquals(sorted(serializer.data.keys()),
                          ['name', 'slug', 'snippets'])


class LanguagesSerializerTestCase(TestCase):
    """
    LanguagesSerializer Test Cases
    """

    def test_valid_serializer(self):
        """
        valid parameters
        """
        languages = Languages.objects.all()[:15]
        serializer = LanguagesSerializer(instance=languages, many=True)
        self.assertIsInstance(serializer.data, list)
        self.assertEquals(len(serializer.data), languages.count())

    def test_snippets_count(self):
        """
        Check pages count
        """
        language = Languages.objects.filter(
            pages__isnull=False).order_by('?')[0]
        serializer = LanguagesSerializer(instance=language)
        self.assertIsInstance(serializer.data, dict)
        self.assertTrue('pages' in serializer.data)
        self.assertEquals(serializer.data['pages'], language.pages_set.count())

    def test_serializer_fields(self):
        """
        Check serializer Fields
        """
        language = Languages.objects.filter(
            pages__isnull=False).order_by('?')[0]
        serializer = LanguagesSerializer(instance=language)
        self.assertIsInstance(serializer.data, dict)
        self.assertEquals(sorted(serializer.data.keys()),
                          ['name', 'pages', 'slug'])