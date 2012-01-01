# -*- coding: utf-8 -*-
from django.test import TestCase
from account.models import User
from account.serializers import UserDetailSerializer
from snippet.models import Snippets, Tags, Languages, Pages, Comments
from snippet.serializers import (SlimSnippetsSerializer, TagsSerializer,
                                 LanguagesSerializer, PagesSerializer,
                                 ComprehensiveSnippetsSerializer,
                                 CommentsSerializer)


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

    def test_snippet_pages(self):
        """
        Check snippet pages count
        """
        snippet = Snippets.objects.filter(pages__isnull=False)[0]
        serializer = SlimSnippetsSerializer(instance=snippet)
        self.assertTrue('pages' in serializer.data)
        self.assertEquals(serializer.data['pages'], snippet.pages_set.count())


class TagsSerializerTestCase(TestCase):
    """
    Tags Serializer Test Cases
    """
    fixtures = ('initial_data', )

    def setUp(self):
        self.tag = Tags.objects.filter(snippets__isnull=False).order_by('?')[0]

    def test_list_serializer(self):
        """
        Serializer data lists
        """
        tags = Tags.objects.all()[:15]
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
                          self.tag.snippets_set.count())

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
    Languages Serializer Test Cases
    """
    fixtures = ('initial_data', )

    def setUp(self):
        self.language = Languages.objects.filter(
            pages__isnull=False).order_by('?')[0]

    def test_list_serializer(self):
        """
        Serializer data lists
        """
        languages = Languages.objects.all()[:15]
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
                          self.language.pages_set.count())

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
    Pages Serializer Test Cases
    """
    fixtures = ('initial_data', )

    def setUp(self):
        self.page = Pages.objects.filter().order_by('?')[0]

    def test_list_serializer(self):
        """
        Serializer data lists
        """
        pages = Pages.objects.filter()[:10]
        serializer = PagesSerializer(instance=pages, many=True)
        self.assertIsInstance(serializer.data, list)
        self.assertEquals(len(serializer.data), pages.count())

    def test_snippet(self):
        """
        Check serializer snippet attr
        """
        serializer = PagesSerializer(instance=self.page)
        self.assertIsInstance(serializer.data, dict)
        self.assertTrue('snippet' in serializer.data)
        self.assertTrue(Snippets.objects.filter(
            slug=serializer.data['snippet']).exists())

    def test_language(self):
        """
        Check serializer language attr
        """
        serializer = PagesSerializer(instance=self.page)
        self.assertIsInstance(serializer.data, dict)
        self.assertTrue('language' in serializer.data)
        self.assertEquals(self.page.language.slug, serializer.data['language'])


class CommentsSerializerTestCase(TestCase):
    """
    Comments Serializer Test Cases
    """
    fixtures = ('initial_data', )

    def setUp(self):
        self.comment = Comments.objects.filter().order_by('?')[0]

    def test_list_serializer(self):
        """
        Serializer data lists
        """
        comments = Comments.objects.all()[:10]
        serializer = CommentsSerializer(instance=comments, many=True)
        self.assertIsInstance(serializer.data, list)
        self.assertEquals(len(serializer.data), comments.count())

    def test_author(self):
        """
        Check serializer author attr.
        """
        serializer = CommentsSerializer(instance=self.comment)
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
        serializer = CommentsSerializer(instance=self.comment)
        snippet_serializer = SlimSnippetsSerializer(
            instance=self.comment.snippet)
        self.assertIsInstance(serializer.data, dict)
        self.assertTrue('snippet' in serializer.data)
        self.assertTrue(Snippets.objects.filter(
            slug=serializer.data['snippet']['slug']).exists())
        self.assertEquals(snippet_serializer.data, serializer.data['snippet'])


class ComprehensiveSnippetsSerializerTestCase(TestCase):
    """
    Comprehensive Snippets Serializer Test Cases
    """

    def test_list_serializer(self):
        """
        Serializer data lists
        """
        snippets = Snippets.objects.all()[:10]
        serializer = ComprehensiveSnippetsSerializer(instance=snippets,
                                                     many=True)
        self.assertIsInstance(serializer.data, list)
        self.assertEquals(len(serializer.data), snippets.count())

    def test_tags(self):
        """
        Check serializer tags attr.
        """
        snippet = Snippets.objects.filter(tags__isnull=False)[0]
        serializer = ComprehensiveSnippetsSerializer(instance=snippet)
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
        snippet = Snippets.objects.filter(pages__isnull=False)[0]
        serializer = ComprehensiveSnippetsSerializer(instance=snippet)
        pages_serializer = PagesSerializer(snippet.pages_set.all(), many=True)
        self.assertIsInstance(serializer.data, dict)
        self.assertTrue('pages' in serializer.data)
        self.assertIsInstance(serializer.data['pages'], list)
        self.assertEquals(len(serializer.data['pages']),
                          snippet.pages_set.count())
        self.assertEquals(pages_serializer.data, serializer.data['pages'])
