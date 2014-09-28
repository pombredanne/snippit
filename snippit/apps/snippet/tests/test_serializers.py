# -*- coding: utf-8 -*-
from django.test import TestCase
from account.models import User
from account.serializers import UserDetailSerializer
from snippet.models import Snippet, Tag, Language, Page, Comment
from rest_framework.test import APIRequestFactory
from snippet.serializers import (SlimSnippetsSerializer, TagsSerializer,
                                 LanguagesSerializer, PagesSerializer,
                                 ComprehensiveSnippetsSerializer,
                                 CommentsSerializer)

factory = APIRequestFactory()
# Just to ensure we have a request in the serializer context
request = factory.get('/')


class SlimSnippetsSerializerTestCase(TestCase):
    """
    Slim SnippetsSerializer Test Cases
    """
    fixtures = ('initial_data', )

    def test_list_serializer(self):
        """
        Serializer data lists
        """
        user = User.objects.filter().order_by('?')[0]
        snippet = Snippet.objects.exclude(user__id=user.id).order_by('?')[0]
        user.stars.add(snippet)
        serializer = SlimSnippetsSerializer(instance=user.stars.all(),
                                            many=True,
                                            context={'request': request})
        self.assertIsInstance(serializer.data, list)
        self.assertEquals(len(serializer.data), user.stars.count())

    def test_snippet_stars(self):
        """
        Check snippet stars count
        """
        user = User.objects.filter().order_by('?')[0]
        snippet = Snippet.objects.exclude(user__id=user.id).order_by('?')[0]
        user.stars.add(snippet)
        serializer = SlimSnippetsSerializer(instance=snippet,
                                            context={'request': request})
        self.assertTrue('stars' in serializer.data)
        self.assertEquals(serializer.data['stars'], snippet.user_set.count())

    def test_snippet_comments(self):
        """
        Check Snippet comments count
        """
        snippet = Snippet.objects.filter(comment__isnull=False)[0]
        serializer = SlimSnippetsSerializer(instance=snippet,
                                            context={'request': request})
        self.assertTrue('comments' in serializer.data)
        self.assertEquals(serializer.data['comments'],
                          snippet.comment_set.count())

    def test_snippet_pages(self):
        """
        Check snippet pages count
        """
        snippet = Snippet.objects.filter(page__isnull=False)[0]
        serializer = SlimSnippetsSerializer(instance=snippet,
                                            context={'request': request})
        self.assertTrue('pages' in serializer.data)
        self.assertEquals(serializer.data['pages'], snippet.page_set.count())


class TagsSerializerTestCase(TestCase):
    """
    Tag Serializer Test Cases
    """
    fixtures = ('initial_data', )

    def setUp(self):
        self.tag = Tag.objects.filter(snippet__isnull=False).order_by('?')[0]

    def test_list_serializer(self):
        """
        Serializer data lists
        """
        tags = Tag.objects.all()[:15]
        serializer = TagsSerializer(instance=tags, many=True)
        self.assertIsInstance(serializer.data, list)
        self.assertEquals(len(serializer.data), tags.count())

    def test_snippets_count(self):
        """
        Check snippets count
        """
        serializer = TagsSerializer(instance=self.tag)
        self.assertIsInstance(serializer.data, dict)
        self.assertTrue('snippets' in serializer.data)
        self.assertEquals(serializer.data['snippets'],
                          self.tag.snippet_set.count())

    def test_serializer_fields(self):
        """
        Check serializer Fields
        """
        serializer = TagsSerializer(instance=self.tag)
        self.assertIsInstance(serializer.data, dict)
        self.assertEquals(sorted(serializer.data.keys()),
                          ['name', 'slug', 'snippets'])


class LanguagesSerializerTestCase(TestCase):
    """
    Language Serializer Test Cases
    """
    fixtures = ('initial_data', )

    def setUp(self):
        self.language = Language.objects.filter(
            page__isnull=False).order_by('?')[0]

    def test_list_serializer(self):
        """
        Serializer data lists
        """
        languages = Language.objects.all()[:15]
        serializer = LanguagesSerializer(instance=languages, many=True)
        self.assertIsInstance(serializer.data, list)
        self.assertEquals(len(serializer.data), languages.count())

    def test_snippets_count(self):
        """
        Check pages count
        """
        serializer = LanguagesSerializer(instance=self.language)
        self.assertIsInstance(serializer.data, dict)
        self.assertTrue('pages' in serializer.data)
        self.assertEquals(serializer.data['pages'],
                          self.language.page_set.count())

    def test_serializer_fields(self):
        """
        Check serializer Fields
        """
        serializer = LanguagesSerializer(instance=self.language)
        self.assertIsInstance(serializer.data, dict)
        self.assertEquals(sorted(serializer.data.keys()),
                          ['name', 'pages', 'slug'])


class PagesSerializerTestCase(TestCase):
    """
    Page Serializer Test Cases
    """
    fixtures = ('initial_data', )

    def setUp(self):
        self.page = Page.objects.filter().order_by('?')[0]

    def test_list_serializer(self):
        """
        Serializer data lists
        """
        pages = Page.objects.filter()[:10]
        serializer = PagesSerializer(instance=pages, many=True)
        self.assertIsInstance(serializer.data, list)
        self.assertEquals(len(serializer.data), pages.count())

    def test_language(self):
        """
        Check serializer language attr
        """
        language_serializer = LanguagesSerializer(
            instance=self.page.language)
        serializer = PagesSerializer(instance=self.page)
        self.assertIsInstance(serializer.data, dict)
        self.assertTrue('language' in serializer.data)
        self.assertIsInstance(serializer.data['language'], dict)
        self.assertEquals(language_serializer.data, serializer.data['language'])


class CommentsSerializerTestCase(TestCase):
    """
    Comment Serializer Test Cases
    """
    fixtures = ('initial_data', )

    def setUp(self):
        self.comment = Comment.objects.filter().order_by('?')[0]

    def test_list_serializer(self):
        """
        Serializer data lists
        """
        comments = Comment.objects.all()[:10]
        serializer = CommentsSerializer(instance=comments, many=True,
                                        context={'request': request})
        self.assertIsInstance(serializer.data, list)
        self.assertEquals(len(serializer.data), comments.count())

    def test_author(self):
        """
        Check serializer author attr.
        """
        serializer = CommentsSerializer(instance=self.comment,
                                        context={'request': request})
        author_serializer = UserDetailSerializer(instance=self.comment.author)
        self.assertIsInstance(serializer.data, dict)
        self.assertTrue('author' in serializer.data)
        self.assertTrue(User.objects.filter(
            username=serializer.data['author']['username']).exists())
        self.assertEquals(author_serializer.data, serializer.data['author'])

    def test_snippet(self):
        """
        Check serializer snippet attr.
        """
        serializer = CommentsSerializer(instance=self.comment,
                                        context={'request': request})
        snippet_serializer = SlimSnippetsSerializer(
            instance=self.comment.snippet, context={'request': request})
        self.assertIsInstance(serializer.data, dict)
        self.assertTrue('snippet' in serializer.data)
        self.assertTrue(Snippet.objects.filter(
            slug=serializer.data['snippet']['slug']).exists())
        self.assertEquals(snippet_serializer.data, serializer.data['snippet'])


class ComprehensiveSnippetsSerializerTestCase(TestCase):
    """
    Comprehensive Snippet Serializer Test Cases
    """

    def test_list_serializer(self):
        """
        Serializer data lists
        """
        snippets = Snippet.objects.all()[:10]
        serializer = ComprehensiveSnippetsSerializer(
            instance=snippets, many=True, context={'request': request})
        self.assertIsInstance(serializer.data, list)
        self.assertEquals(len(serializer.data), snippets.count())

    def test_tags(self):
        """
        Check serializer tags attr.
        """
        snippet = Snippet.objects.filter(tag__isnull=False)[0]
        serializer = ComprehensiveSnippetsSerializer(
            instance=snippet, context={'request': request})
        tags_serializer = TagsSerializer(instance=snippet.tags.all(), many=True)
        self.assertIsInstance(serializer.data, dict)
        self.assertTrue('tags' in serializer.data)
        self.assertIsInstance(serializer.data['tags'], list)
        self.assertEquals(len(serializer.data['tags']), snippet.tags.count())
        self.assertEquals(tags_serializer.data, serializer.data['tags'])

    def test_pages(self):
        """
        Check serializer pages attr.
        """
        snippet = Snippet.objects.filter(page__isnull=False)[0]
        serializer = ComprehensiveSnippetsSerializer(
            instance=snippet, context={'request': request})
        pages_serializer = PagesSerializer(snippet.page_set.all(), many=True)
        self.assertIsInstance(serializer.data, dict)
        self.assertTrue('pages' in serializer.data)
        self.assertIsInstance(serializer.data['pages'], list)
        self.assertEquals(len(serializer.data['pages']),
                          snippet.page_set.count())
        self.assertEquals(pages_serializer.data, serializer.data['pages'])
