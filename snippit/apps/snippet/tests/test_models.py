# -*- coding: utf-8 -*-
from django.test import TestCase
from snippet.models import Comment, Language, Snippet, Page, Tag
from account.models import User
from django.db.utils import IntegrityError


class TagsTestCase(TestCase):
    """
    Tag model test cases
    """

    fixtures = ('initial_data', )

    def test_tag_creation(self):
        """
        Create Tag
        """
        tag = Tag.objects.create(name='test')
        self.assertIsNotNone(tag.id)
        self.assertIsNotNone(Tag.objects.get(id=tag.id).slug)
        self.assertEqual(Tag.objects.filter(slug=tag.slug).count(), 1)
        self.assertEqual(Tag.objects.get(id=tag.id).name, tag.name)

    def test_unique_slug_check(self):
        """
        slug attribute must be unique
        """
        tag1 = Tag.objects.create(name='testslug')
        tag2 = Tag.objects.create(name='testslug')
        self.assertTrue(Tag.objects.filter(slug=tag1.slug).exists())
        self.assertTrue(Tag.objects.filter(slug=tag2.slug).exists())
        self.assertNotEqual(tag1.slug, tag2.slug)
        self.assertEqual(tag1.name, tag2.name)

    def test_tag_delete(self):
        """
        Delete Slug
        """
        tag = Tag.objects.filter().order_by('?')[0]
        tag.delete()
        self.assertFalse(Tag.objects.filter(slug=tag.slug).exists())
        self.assertFalse(Snippet.objects.filter(tag__in=(tag.id,)).exists())


class LanguageTestCase(TestCase):
    """
    Language model test cases
    """

    fixtures = ('initial_data', )

    def test_language_creation(self):
        """
        Create language (Programming Language)
        """
        lang = Language.objects.create(name='test')
        self.assertIsNotNone(lang.id)
        self.assertEqual(Language.objects.filter(id=lang.id).count(), 1)
        self.assertIsNotNone(Language.objects.get(id=lang.id).slug)
        self.assertEqual(Language.objects.get(id=lang.id).name, lang.name)

    def test_unique_slug_check(self):
        """
        slug attribute must be unique
        """
        lang1 = Language.objects.create(name='java')
        lang2 = Language.objects.create(name='java')
        self.assertTrue(Language.objects.filter(slug=lang1.slug).exists())
        self.assertTrue(Language.objects.filter(slug=lang2.slug).exists())
        self.assertNotEqual(lang1.slug, lang2.slug)
        self.assertEqual(lang1.name, lang2.name)

    def test_language_delete(self):
        """
        Delete Language
        """
        lang = Language.objects.filter().order_by('?')[0]
        lang.delete()
        self.assertFalse(Language.objects.filter(slug=lang.slug).exists())
        self.assertFalse(Page.objects.filter(language__id=lang.id).exists())


class SnippetsTestCase(TestCase):
    """
    Snippet model test cases
    """
    fixtures = ('initial_data', )

    def test_create_snippet(self):
        """
        Create Code Snippet
        """
        user = User.objects.filter().order_by('?')[0]
        snippet = Snippet.objects.create(name='Django Transaction Example',
                                          created_by=user, is_public=True)
        self.assertIsNotNone(snippet.id)
        self.assertTrue(Snippet.objects.filter(
            id=snippet.id, created_by=user, is_public=True).exists())
        # check slug
        self.assertEqual(Snippet.objects.filter(slug=snippet.slug).count(), 1)
        self.assertEqual(Snippet.objects.get(id=snippet.id).name, snippet.name)
        # check created date
        self.assertIsNotNone(Snippet.objects.get(
            slug=snippet.slug).created_at)
        # tags must be empty
        self.assertEqual(Snippet.objects.get(
            id=snippet.id).tags.exists(), False)

    def test_delete_snippet(self):
        """
        Delete Code Snippet
        """
        snippet = Snippet.objects.filter().order_by('?')[0]
        snippet.delete()
        self.assertFalse(Snippet.objects.filter(id=snippet.id).exists())
        # check relations
        self.assertFalse(Page.objects.filter(snippet__id=snippet.id).exists())
        self.assertFalse(Comment.objects.filter(
            snippet__id=snippet.id).exists())

    def test_snippet_subscribers(self):
        snippet = Snippet.objects.filter(
            subscribers__isnull=True).order_by('?')[0]
        self.subscribe_user = User.objects.filter().order_by('?')[0]
        snippet.subscribers.add(self.subscribe_user)
        self.assertTrue(snippet.subscribers.exists())
        self.assertTrue(snippet.subscribers.filter(
            id=self.subscribe_user.id).exists())

    def test_snippet_remove_subscribe(self):
        self.test_snippet_subscribers()
        snippet = Snippet.objects.filter(
            subscribers__isnull=False).order_by('?')[0]
        count = snippet.subscribers.count()
        snippet.subscribers.remove(self.subscribe_user)
        self.assertFalse(snippet.subscribers.filter(
            id=self.subscribe_user.id).exists())
        self.assertNotEqual(count, snippet.subscribers.count())

    def test_update_snippet(self):
        """
        Update Code Snippet
        """
        snippet = Snippet.objects.filter().order_by('?')[0]
        updated_at = snippet.updated_at
        snippet.name = 'Knockout Js Example'
        snippet.save()
        self.assertTrue(Snippet.objects.filter(
            id=snippet.id, name=snippet.name).exists())
        self.assertNotEqual(Snippet.objects.get(id=snippet.id).updated_at,
                            updated_at)
        # slug not editable
        self.assertEqual(Snippet.objects.get(id=snippet.id).slug, snippet.slug)

    def test_required_created_by_check(self):
        """
        Created user must be required
        """
        self.assertRaisesMessage(IntegrityError,
                                 'snippets.created_by_id may not be NULL',
                                 Snippet.objects.create,
                                 name='Test', is_public=True)


class PagesTestCase(TestCase):
    """
    Page model test cases
    """
    fixtures = ('initial_data', )

    def test_create_page(self):
        """
        Create Snippet Page
        """
        snippet = Snippet.objects.filter().order_by('?')[0]
        language = Language.objects.filter().order_by('?')[0]
        page = Page.objects.create(snippet=snippet, language=language,
                                    content='test page')
        self.assertIsNotNone(page.id)
        self.assertTrue(Page.objects.filter(id=page.id, language=language,
                                             content='test page').exists())

    def test_update_page(self):
        """
        Update Page
        """
        page = Page.objects.filter().order_by('?')[0]
        language = Language.objects.exclude(id=page.language.id)\
                                    .order_by('?')[0]
        page.language = language
        page.save()
        self.assertTrue(Page.objects.filter(
            id=page.id, language=language).exists())

    def test_delete_page(self):
        """
        Delete Code Snippet Page
        """
        page = Page.objects.filter().order_by('?')[0]
        page.delete()
        self.assertFalse(Page.objects.filter(id=page.id).exists())


class CommentsTestCase(TestCase):
    """
    Comment model test cases
    """

    fixtures = ('initial_data', )

    def test_create_comment(self):
        """
        Create Comment
        """
        user = User.objects.filter().order_by('?')[0]
        snippet = Snippet.objects.filter().order_by('?')[0]
        comment = Comment.objects.create(author=user, snippet=snippet,
                                          comment='Test Comment')
        self.assertIsNotNone(comment.id)
        self.assertIsNotNone(Comment.objects.get(id=comment.id).created_at)
        self.assertTrue(Comment.objects.filter(id=comment.id, author=user,
                                                snippet=snippet).exists())

    def test_delete_comment(self):
        """
        Delete Comment
        """
        comment = Comment.objects.filter().order_by('?')[0]
        comment.delete()
        self.assertFalse(Comment.objects.filter(id=comment.id).exists())

    def test_required_author_check(self):
        """
        author must be required
        """
        snippet = Snippet.objects.filter().order_by('?')[0]
        self.assertRaisesMessage(IntegrityError,
                                 'snippets_comments.author_id may not be NULL',
                                 Comment.objects.create,
                                 snippet=snippet, comment='Test Comment')

    def test_required_snippet_check(self):
        """
        Snippet must be required
        """
        user = User.objects.filter().order_by('?')[0]
        self.assertRaisesMessage(IntegrityError,
                                 'snippets_comments.snippet_id may not be NULL',
                                 Comment.objects.create,
                                 author=user, comment='Test Comment')
