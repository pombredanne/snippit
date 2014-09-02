# -*- coding: utf-8 -*-
from django.test import TestCase
from snippet.models import Comments, Languages, Snippets, Pages, Tags
from account.models import User
from django.db.utils import IntegrityError


class TagsTestCase(TestCase):
    """
    Tags model test cases
    """

    fixtures = ('initial_data', )

    def test_tag_creation(self):
        """
        Create Tag
        """
        tag = Tags.objects.create(name='test')
        self.assertIsNotNone(tag.id)
        self.assertIsNotNone(Tags.objects.get(id=tag.id).slug)
        self.assertEqual(Tags.objects.filter(slug=tag.slug).count(), 1)
        self.assertEqual(Tags.objects.get(id=tag.id).name, tag.name)

    def test_unique_slug_check(self):
        """
        slug attribute must be unique
        """
        tag1 = Tags.objects.create(name='testslug')
        tag2 = Tags.objects.create(name='testslug')
        self.assertTrue(Tags.objects.filter(slug=tag1.slug).exists())
        self.assertTrue(Tags.objects.filter(slug=tag2.slug).exists())
        self.assertNotEqual(tag1.slug, tag2.slug)
        self.assertEqual(tag1.name, tag2.name)

    def test_tag_delete(self):
        """
        Delete Slug
        """
        tag = Tags.objects.filter().order_by('?')[0]
        tag.delete()
        self.assertFalse(Tags.objects.filter(slug=tag.slug).exists())
        self.assertFalse(Snippets.objects.filter(tags__in=(tag.id,)).exists())


class LanguageTestCase(TestCase):
    """
    Language model test cases
    """

    fixtures = ('initial_data', )

    def test_language_creation(self):
        """
        Create language (Programming Language)
        """
        lang = Languages.objects.create(name='test')
        self.assertIsNotNone(lang.id)
        self.assertEqual(Languages.objects.filter(id=lang.id).count(), 1)
        self.assertIsNotNone(Languages.objects.get(id=lang.id).slug)
        self.assertEqual(Languages.objects.get(id=lang.id).name, lang.name)

    def test_unique_slug_check(self):
        """
        slug attribute must be unique
        """
        lang1 = Languages.objects.create(name='java')
        lang2 = Languages.objects.create(name='java')
        self.assertTrue(Languages.objects.filter(slug=lang1.slug).exists())
        self.assertTrue(Languages.objects.filter(slug=lang2.slug).exists())
        self.assertNotEqual(lang1.slug, lang2.slug)
        self.assertEqual(lang1.name, lang2.name)

    def test_language_delete(self):
        """
        Delete Language
        """
        lang = Languages.objects.filter().order_by('?')[0]
        lang.delete()
        self.assertFalse(Languages.objects.filter(slug=lang.slug).exists())
        self.assertFalse(Pages.objects.filter(language__id=lang.id).exists())


class SnippetsTestCase(TestCase):
    """
    Snippets model test cases
    """
    fixtures = ('initial_data', )

    def test_create_snippet(self):
        """
        Create Code Snippet
        """
        user = User.objects.filter().order_by('?')[0]
        snippet = Snippets.objects.create(name='Django Transaction Example',
                                          created_by=user, is_public=True)
        self.assertIsNotNone(snippet.id)
        self.assertTrue(Snippets.objects.filter(
            id=snippet.id, created_by=user, is_public=True).exists())
        # check slug
        self.assertEqual(Snippets.objects.filter(slug=snippet.slug).count(), 1)
        self.assertEqual(Snippets.objects.get(id=snippet.id).name, snippet.name)
        # check created date
        self.assertIsNotNone(Snippets.objects.get(
            slug=snippet.slug).created_at)
        # tags must be empty
        self.assertEqual(Snippets.objects.get(
            id=snippet.id).tags.exists(), False)

    def test_delete_snippet(self):
        """
        Delete Code Snippet
        """
        snippet = Snippets.objects.filter().order_by('?')[0]
        snippet.delete()
        self.assertFalse(Snippets.objects.filter(id=snippet.id).exists())
        # check relations
        self.assertFalse(Pages.objects.filter(snippet__id=snippet.id).exists())
        self.assertFalse(Comments.objects.filter(
            snippet__id=snippet.id).exists())

    def test_snippet_subscribers(self):
        snippet = Snippets.objects.filter(
            subscribers__isnull=True).order_by('?')[0]
        self.subscribe_user = User.objects.filter().order_by('?')[0]
        snippet.subscribers.add(self.subscribe_user)
        self.assertTrue(snippet.subscribers.exists())
        self.assertTrue(snippet.subscribers.filter(
            id=self.subscribe_user.id).exists())

    def test_snippet_remove_subscribe(self):
        self.test_snippet_subscribers()
        snippet = Snippets.objects.filter(
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
        snippet = Snippets.objects.filter().order_by('?')[0]
        updated_at = snippet.updated_at
        snippet.name = 'Knockout Js Example'
        snippet.save()
        self.assertTrue(Snippets.objects.filter(
            id=snippet.id, name=snippet.name).exists())
        self.assertNotEqual(Snippets.objects.get(id=snippet.id).updated_at,
                            updated_at)
        # slug not editable
        self.assertEqual(Snippets.objects.get(id=snippet.id).slug, snippet.slug)

    def test_required_created_by_check(self):
        """
        Created user must be required
        """
        self.assertRaisesMessage(IntegrityError,
                                 'snippets.created_by_id may not be NULL',
                                 Snippets.objects.create,
                                 name='Test', is_public=True)


class PagesTestCase(TestCase):
    """
    Pages model test cases
    """
    fixtures = ('initial_data', )

    def test_create_page(self):
        """
        Create Snippet Page
        """
        snippet = Snippets.objects.filter().order_by('?')[0]
        language = Languages.objects.filter().order_by('?')[0]
        page = Pages.objects.create(snippet=snippet, language=language,
                                    content='test page')
        self.assertIsNotNone(page.id)
        self.assertTrue(Pages.objects.filter(id=page.id, language=language,
                                             content='test page').exists())

    def test_update_page(self):
        """
        Update Page
        """
        page = Pages.objects.filter().order_by('?')[0]
        language = Languages.objects.exclude(id=page.language.id)\
                                    .order_by('?')[0]
        page.language = language
        page.save()
        self.assertTrue(Pages.objects.filter(
            id=page.id, language=language).exists())

    def test_delete_page(self):
        """
        Delete Code Snippet Page
        """
        page = Pages.objects.filter().order_by('?')[0]
        page.delete()
        self.assertFalse(Pages.objects.filter(id=page.id).exists())


class CommentsTestCase(TestCase):
    """
    Comments model test cases
    """

    fixtures = ('initial_data', )

    def test_create_comment(self):
        """
        Create Comment
        """
        user = User.objects.filter().order_by('?')[0]
        snippet = Snippets.objects.filter().order_by('?')[0]
        comment = Comments.objects.create(author=user, snippet=snippet,
                                          comment='Test Comment')
        self.assertIsNotNone(comment.id)
        self.assertIsNotNone(Comments.objects.get(id=comment.id).created_at)
        self.assertTrue(Comments.objects.filter(id=comment.id, author=user,
                                                snippet=snippet).exists())

    def test_delete_comment(self):
        """
        Delete Comment
        """
        comment = Comments.objects.filter().order_by('?')[0]
        comment.delete()
        self.assertFalse(Comments.objects.filter(id=comment.id).exists())

    def test_required_author_check(self):
        """
        author must be required
        """
        snippet = Snippets.objects.filter().order_by('?')[0]
        self.assertRaisesMessage(IntegrityError,
                                 'snippets_comments.author_id may not be NULL',
                                 Comments.objects.create,
                                 snippet=snippet, comment='Test Comment')

    def test_required_snippet_check(self):
        """
        Snippet must be required
        """
        user = User.objects.filter().order_by('?')[0]
        self.assertRaisesMessage(IntegrityError,
                                 'snippets_comments.snippet_id may not be NULL',
                                 Comments.objects.create,
                                 author=user, comment='Test Comment')
