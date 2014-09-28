# -*- coding: utf-8 -*-
import simplejson

from django.test import TestCase
from account.models import User
from snippet.models import Tag, Language, Snippet, Comment
from snippet.serializers import TagsSerializer, LanguagesSerializer
from snippit.core.mixins import RestApiScenarioMixin
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core import mail


class TagsViewTestCase(RestApiScenarioMixin, TestCase):
    """
    TagsView Test Cases
    """
    fixtures = ('initial_data', )

    @classmethod
    def setUpClass(cls):
        cls.key = settings.REST_FRAMEWORK['PAGINATE_BY_PARAM']
        cls.limit = settings.REST_FRAMEWORK['PAGINATE_BY']
        cls.url = reverse('tags-list')

    def test_tags_list(self):
        """
        Tag list
        """
        self.assertListResource(url=self.url, queryset=Tag.objects.all())

    def test_tags_limit(self):
        """
        Check Tag per limit
        """
        content = self.assertListResource(self.url, queryset=Tag.objects.all(),
                                          data={self.key: 1})
        self.assertEqual(len(content.get('results')), 1)

    def test_tags_sort(self):
        """
        Key based Sort
        """
        content = self.assertListResource(self.url, queryset=Tag.objects.all(),
                                          data={'ordering': '-snippets',
                                                self.key: 1})
        self.assertEquals(len(content['results']), 1)
        self.assertTrue(Tag.objects.filter(
            slug=content['results'][0]['slug']).exists())
        self.assertEquals(content['results'][0]['snippets'],
                          Tag.objects.get(
                              slug=content['results'][0]['slug'])
                          .snippet_set.count())
        self.assertEquals(content['results'][0]['slug'],
                          Tag.objects.filter().order_by('-snippets')[0].slug)

    def test_tags_filtering(self):
        """
        Tag Filtering test
        """
        tag = Tag.objects.filter().order_by('?')[0]
        check_data = Tag.objects.filter(
            name__icontains=tag.name).order_by('-name')[:10]
        # match data
        serializer = TagsSerializer(instance=check_data, many=True)
        content = self.assertListResource(
            self.url, queryset=check_data, data={'ordering': '-name',
                                                 self.key: 10,
                                                 'search': tag.name},)
        self.assertEquals(len(content['results']), check_data.count())
        self.assertEquals(content['results'], serializer.data)


class LanguagesViewTestCase(RestApiScenarioMixin, TestCase):
    """
    LanguagesView Test Cases
    """
    fixtures = ('initial_data', )

    @classmethod
    def setUpClass(cls):
        cls.key = settings.REST_FRAMEWORK['PAGINATE_BY_PARAM']
        cls.limit = settings.REST_FRAMEWORK['PAGINATE_BY']
        cls.url = reverse('languages-list')

    def test_languages_list(self):
        """
        Language list
        """
        self.assertListResource(url=self.url, queryset=Language.objects.all())

    def test_languages_limit(self):
        """
        Check Tag per limit
        """
        content = self.assertListResource(self.url, data={self.key: 1},
                                          queryset=Language.objects.all())
        self.assertEqual(len(content.get('results')), 1)

    def test_languages_sort(self):
        """
        Key based Sort
        """
        content = self.assertListResource(self.url,
                                          queryset=Language.objects.all(),
                                          data={'ordering': '-pages',
                                                self.key: 1})
        self.assertEquals(len(content['results']), 1)
        self.assertTrue(Language.objects.filter(
            slug=content['results'][0]['slug']).exists())
        self.assertEquals(content['results'][0]['pages'],
                          Language.objects.get(
                              slug=content['results'][0]['slug'])
                          .page_set.count())
        self.assertEquals(content['results'][0]['slug'],
                          Language.objects.filter().order_by('-pages')[0].slug)

    def test_language_filtering(self):
        """
        star ordered to the user's snippets
        """
        language = Language.objects.filter().order_by('?')[0]
        check_data = Language.objects.filter(
            name__icontains=language.name).order_by('-name')[:10]
        # match data
        serializer = LanguagesSerializer(instance=check_data, many=True)
        content = self.assertListResource(
            self.url, queryset=check_data, data={'ordering': '-name',
                                                 self.key: 10,
                                                 'search': language.name})
        self.assertEquals(len(content['results']), check_data.count())
        self.assertEquals(content['results'], serializer.data)


class TagSnippetsViewsTestCase(RestApiScenarioMixin, TestCase):
    """
    TagSnippetsViews TestCase
    """

    fixtures = ('initial_data', )

    def setUp(self):
        self.tag = Tag.objects.filter(snippet__isnull=False)[0]
        self.url = reverse('tag-snippets-list', args=[self.tag.slug])
        super(TagSnippetsViewsTestCase, self).setUp()

    def test_tag_snippets_list(self):
        """
        Tag Snippet list
        """
        self.assertListResource(url=self.url,
                                queryset=self.tag.snippet_set.all())

    def test_invalid_tag(self):
        """
        Invalid tag can not be snippets
        """
        self.assertInvalidObjectResource('tag-snippets-list')

    def test_tag_empty_snippets(self):
        self.tag.snippets_set.all().delete()
        content = self.assertListResource(self.url,
                                          queryset=self.tag.snippet_set.all())
        self.assertGreaterEqual(len(content['results']), 0)


class LanguageSnippetsViewTestCase(RestApiScenarioMixin, TestCase):
    """
    LanguageSnippetsView TestCase
    """

    fixtures = ('initial_data', )

    def setUp(self):
        self.language = Language.objects.filter(page__isnull=False)[0]
        self.snippets = Snippet.objects.filter(
            page__language__id=self.language.id)
        self.url = reverse('language-snippets-list', args=[self.language.slug])
        super(LanguageSnippetsViewTestCase, self).setUp()

    def test_language_snippets_list(self):
        self.assertListResource(url=self.url, queryset=self.snippets)

    def test_invalid_language(self):
        self.assertInvalidObjectResource('language-snippets-list')


class SnippetsViewTestCase(RestApiScenarioMixin, TestCase):
    """
    SnippetsView TestCase
    """

    fixtures = ('initial_data', )
    
    def setUp(self):
        self.url = reverse('snippets-list')
        self.user = User.objects.filter(snippet__isnull=True).order_by('?')[0]
        self.snippet = Snippet.objects.filter().order_by('?')[0]
        self.data = {
            "public": True,
            "pages": [
                {"content": "Hello World", "language": "javascript"}
            ],
            "name": "JS Test",
            "tags": [
                "java"
            ]
        }
        super(SnippetsViewTestCase, self).setUp()

    def test_list_snippets(self):
        content = self.assertListResource(url=self.url,
                                          queryset=Snippet.objects.all())
        last_snippet = Snippet.objects.filter().order_by('-id')[0]
        self.assertEqual(content.get("results")[0]['slug'], last_snippet.slug)

    def test_create_snippet_unverified_user(self):
        response = self.c.post(self.url, simplejson.dumps(self.data),
                               content_type='application/json')
        self.assertHttpUnauthorized(response)

    def test_create_snippet_required_fields_be_empty(self):
        self.token_login()
        response = self.c.post(self.url, content_type='application/json',
                               **self.client_header)
        content = simplejson.loads(response.content)
        self.assertHttpBadRequest(response)
        self.assertEquals(sorted(content.keys()), ['name', 'pages', 'public'])

    def test_create_snippet_invalid_tag(self):
        self.data['tags'][0] = '??'
        self.token_login()
        response = self.c.post(self.url, simplejson.dumps(self.data),
                               content_type='application/json',
                               **self.client_header)
        content = simplejson.loads(response.content)
        self.assertHttpBadRequest(response)
        self.assertEquals(sorted(content.keys()), ['tags'])
        self.assertEqual(content['tags'][0],
                         "Enter a valid 'slug' consisting of "
                         "letters, numbers, underscores "
                         "or hyphens.")

    def test_create_snippet_invalid_language(self):
        self.data['pages'][0]['language'] = 'hede'
        self.token_login()
        response = self.c.post(self.url, simplejson.dumps(self.data),
                               content_type='application/json',
                               **self.client_header)
        content = simplejson.loads(response.content)
        self.assertHttpBadRequest(response)
        self.assertEquals(sorted(content.keys()), ['pages'])
        self.assertEqual(content['pages'][0].keys(), ['language'])
        self.assertEqual(content['pages'][0]['language'],
                         ["Object with slug=%s does not "
                          "exist." % self.data['pages'][0]['language']])

    def test_create_snippet(self):
        self.token_login()
        response = self.c.post(self.url, simplejson.dumps(self.data),
                               content_type='application/json',
                               **self.client_header)
        content = simplejson.loads(response.content)
        self.assertHttpCreated(response)
        self.assertTrue(Snippet.objects.filter(slug=content['slug']).exists())
        self.assertTrue(Tag.objects.filter(
            name__in=self.data['tags']).exists())
        self.assertTrue(Snippet.objects.get(
            slug=content['slug']).page_set.exists())


class SnippetDetailViewTestCase(RestApiScenarioMixin, TestCase):
    """
    SnippetDetailView Test Cases
    """
    fixtures = ('initial_data', )

    def setUp(self):
        self.snippet = Snippet.objects.filter().order_by('?')[0]
        self.url = reverse('snippets-detail', args=[self.snippet.slug])
        self.user = self.snippet.created_by
        self.user.set_password('123456')
        self.user.save()
        self.data = {
            "public": True,
            "pages": [
                {"content": "Hello World", "language": "javascript"}
            ],
            "name": "JS Test",
            "tags": [
                "java"
            ]
        }
        super(SnippetDetailViewTestCase, self).setUp()

    def test_snippet_detail(self):
        response = self.c.get(path=self.url, content_type='application/json')
        content = simplejson.loads(response.content)
        self.assertHttpOk(response)
        self.assertEqual(content['name'], self.snippet.name)
        self.assertEqual(content['slug'], self.snippet.slug)
        self.assertEqual(len(content['tags']), self.snippet.tags.count())
        self.assertEqual(len(content['pages']), self.snippet.page_set.count())
        self.assertEqual(content['public'], self.snippet.is_public)

    def test_invalid_snippet(self):
        self.assertInvalidObjectResource('snippets-detail')

    def test_update_other_user_snippet(self):
        self.token_login()
        response = self.c.put(self.url, simplejson.dumps(self.data),
                              content_type='application/json',
                              **self.client_header)
        self.assertHttpForbidden(response)

    def test_update_snippet(self):
        self.token_login(username=self.user.username, password='123456')
        response = self.c.put(self.url, simplejson.dumps(self.data),
                              content_type='application/json',
                              **self.client_header)
        self.assertHttpOk(response)
        self.assertTrue(self.snippet.tags.filter(
            name__in=self.data['tags']).exists())
        self.assertEqual(Snippet.objects.get(id=self.snippet.id).name,
                         self.data['name'])

    def test_update_snippet_add_page(self):
        self.token_login(username=self.user.username, password='123456')
        count = self.snippet.page_set.count()
        self.data['pages'].append({"content": "Hello World",
                                   "language": "javascript"})
        response = self.c.put(self.url, simplejson.dumps(self.data),
                              content_type='application/json',
                              **self.client_header)
        self.assertHttpOk(response)
        self.assertEqual(Snippet.objects.get(
            id=self.snippet.id).page_set.count(), count + 1)

    def test_update_unverified_user(self):
        response = self.c.put(self.url, simplejson.dumps(self.data),
                              content_type='application/json',
                              **self.client_header)
        self.assertHttpUnauthorized(response)

    def test_destroy_snippet(self):
        self.token_login(username=self.user.username, password='123456')
        response = self.c.delete(self.url, content_type='application/json',
                                 **self.client_header)
        self.assertHttpNoContent(response)
        self.assertFalse(Snippet.objects.filter(id=self.snippet.id).exists())


class SnippetStarViewTestCase(RestApiScenarioMixin, TestCase):
    """
    SnippetStarView Test Cases
    """
    fixtures = ('initial_data', )

    def test_check_if_a_snippet_is_starred_for_not_starred_snippet(self):
        self.token_login()
        snippet = Snippet.objects.filter().order_by('?')[0]
        url = reverse('snippets-star', args=[snippet.slug])
        response = self.c.get(url, **self.client_header)
        self.assertHttpOk(response)

    def test_check_if_a_snippet_is_starred_for_starred_snippet(self):
        self.token_login()
        snippet = Snippet.objects.filter().order_by('?')[0]
        self.u.stars.add(snippet)
        url = reverse('snippets-star', args=[snippet.slug])
        response = self.c.get(url, **self.client_header)
        self.assertHttpNoContent(response)

    def test_invalid_snippet(self):
        self.assertInvalidObjectResource('snippets-star', auth=True)

    def test_star_snippet(self):
        self.token_login()
        snippet = Snippet.objects.filter().order_by('?')[0]
        url = reverse('snippets-star', args=[snippet.slug])
        response = self.c.post(url, **self.client_header)
        self.assertHttpCreated(response)
        self.assertTrue(self.u.stars.exists())

    def test_unstar_snippet(self):
        self.token_login()
        snippet = Snippet.objects.filter().order_by('?')[0]
        self.u.stars.add(snippet)
        url = reverse('snippets-star', args=[snippet.slug])
        response = self.c.delete(url, **self.client_header)
        self.assertHttpNoContent(response)
        self.assertFalse(self.u.stars.exists())

    def test_already_star_for_starred(self):
        self.token_login()
        snippet = Snippet.objects.filter().order_by('?')[0]
        url = reverse('snippets-star', args=[snippet.slug])
        self.u.stars.add(snippet)
        response = self.c.post(url, **self.client_header)
        self.assertHttpForbidden(response)

    def test_unstar_for_not_starred_snippet(self):
        self.token_login()
        snippet = Snippet.objects.filter().order_by('?')[0]
        url = reverse('snippets-star', args=[snippet.slug])
        response = self.c.delete(url, **self.client_header)
        self.assertHttpForbidden(response)

    def test_star_snippet_unverified_user(self):
        snippet = Snippet.objects.filter().order_by('?')[0]
        url = reverse('snippets-star', args=[snippet.slug])
        response = self.c.post(url, **self.client_header)
        self.assertHttpUnauthorized(response)


class SnippetCommentsViewTestCase(RestApiScenarioMixin, TestCase):
    """
    SnippetCommentsView Test Cases
    """
    fixtures = ('initial_data', )

    def setUp(self):
        self.snippet = Snippet.objects.filter(comment__isnull=False)[0]
        self.url = reverse('snippets-comments', args=[self.snippet.slug])
        super(SnippetCommentsViewTestCase, self).setUp()

    def test_snippet_comments(self):
        self.assertListResource(self.url,
                                queryset=self.snippet.comment_set.all())

    def test_invalid_snippet(self):
        self.assertInvalidObjectResource('snippets-comments', auth=True)

    def test_create_comment_for_unverified_user(self):
        response = self.c.post(self.url)
        self.assertHttpUnauthorized(response)

    def test_create_comment(self):
        data = {
            'comment': 'test comment'
        }
        self.token_login()
        response = self.c.post(self.url, simplejson.dumps(data),
                               content_type='application/json',
                               **self.client_header)
        self.assertHttpCreated(response)
        self.assertTrue(self.u.comment_set.exists())
        self.assertTrue(Comment.objects.filter(
            comment=data['comment']).exists())
        self.assertTrue(self.snippet.comment_set.exists())
        # check signal
        self.assertGreater(mail.outbox, 0)


class SnippetStarredUsersViewTestCase(RestApiScenarioMixin, TestCase):
    """
    SnippetStarredUsersView Test Cases
    """
    fixtures = ('initial_data', )

    def test_list_snippet_starred_users(self):
        snippet = Snippet.objects.filter(comment__isnull=False)[0]
        self.u.stars.add(snippet)
        url = reverse('snippets-starred-users', args=[snippet.slug])
        self.assertListResource(url=url, queryset=snippet.user_set.all())

    def test_invalid_snippet(self):
        self.assertInvalidObjectResource('snippets-starred-users')


class SnippetSubscribeTestCase(RestApiScenarioMixin, TestCase):
    """
    Snippet Subscribe Test Cases
    """
    fixtures = ('initial_data', )

    def setUp(self):
        self.snippet = Snippet.objects.filter().order_by('?')[0]
        self.other_user = User.objects.filter(
            subscribed__isnull=True).order_by('?')[0]
        self.snippet.subscribers.add(self.other_user)
        self.url = reverse('snippets-subscribers', args=[self.snippet.slug])
        super(SnippetSubscribeTestCase, self).setUp()

    def test_snippet_subscribers_list(self):
        self.assertListResource(queryset=self.snippet.subscribers.all(),
                                url=self.url)

    def test_undefined_snippet_subscribers_list(self):
        self.assertInvalidObjectResource(
            url=reverse('snippets-subscribers', args=['asd-ddsds']))

    def test_snippet_subscribe_for_unverified_user(self):
        response = self.c.post(self.url, content_type='application/json')
        self.assertHttpUnauthorized(response)

    def test_snippet_un_subscribe_for_unverified_user(self):
        response = self.c.delete(self.url, content_type='application/json',)
        self.assertHttpUnauthorized(response)

    def test_snippet_subscribe(self):
        self.snippet.subscribers.clear()
        self.token_login()
        response = self.c.post(self.url, content_type='application/json',
                               **self.client_header)
        self.assertHttpCreated(response)
        self.assertTrue(self.snippet.subscribers.filter(id=self.u.id).exists())

    def test_snippet_un_subscribe(self):
        self.snippet.subscribers.clear()
        self.test_snippet_subscribe()
        response = self.c.delete(self.url, content_type='application/json',
                                 **self.client_header)
        self.assertHttpNoContent(response)
        self.assertFalse(self.snippet.subscribers.filter(id=self.u.id).exists())

    def test_already_subscribe(self):
        self.snippet.subscribers.clear()
        self.test_snippet_subscribe()
        response = self.c.post(self.url, content_type='application/json',
                               **self.client_header)
        data = simplejson.loads(response.content)
        self.assertHttpConflict(response)
        self.assertEqual(data['detail'], 'User already exists.')

    def test_not_subscribed_un_subscribe(self):
        user = User.objects.filter(subscribed__isnull=True).order_by('?')[0]
        user.set_password('123456')
        user.save()
        self.token_login(username=user.username, password='123456')
        response = self.c.delete(self.url, content_type='application/json',
                                 **self.client_header)
        data = simplejson.loads(response.content)
        self.assertHttpNotFound(response)
        self.assertEqual(data['detail'], 'User does not between subscribers')
