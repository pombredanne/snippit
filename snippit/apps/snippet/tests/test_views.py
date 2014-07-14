# -*- coding: utf-8 -*-
import simplejson

from django.test import TestCase
from account.models import User
from snippet.models import Tags, Languages, Snippets
from snippet.serializers import TagsSerializer, LanguagesSerializer
from snippit.core.mixins import CommonTestMixin, HttpStatusCodeMixin
from django.core.urlresolvers import reverse
from django.conf import settings


class TagsViewTestCase(CommonTestMixin, HttpStatusCodeMixin, TestCase):
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
        Tags list
        """
        response = self.c.get(self.url, content_type='application/json')
        content = simplejson.loads(response.content)
        self.assertHttpOk(response)
        self.assertIsInstance(content, dict)
        self.assertIsInstance(content['results'], list)
        self.assertEquals(len(content['results']), self.limit)
        self.assertEquals(content['count'], Tags.objects.count())

    def test_tags_limit(self):
        """
        Check Tags per limit
        """
        response = self.c.get(self.url, data={self.key: 100},
                              content_type='application/json')
        content = simplejson.loads(response.content)
        self.assertHttpOk(response)
        self.assertEquals(content['count'], Tags.objects.count())
        self.assertGreater(len(content['results']), self.limit)
        self.assertIsInstance(content['results'], list)

    def test_tags_sort(self):
        """
        Key based Sort
        """
        # desc sorting
        response = self.c.get(self.url, content_type='application/json',
                              data={'ordering': '-snippets', self.key: 1})
        content = simplejson.loads(response.content)
        self.assertHttpOk(response)
        self.assertEquals(content['count'], Tags.objects.count())
        self.assertIsInstance(content['results'], list)
        self.assertEquals(len(content['results']), 1)
        self.assertTrue(Tags.objects.filter(
            slug=content['results'][0]['slug']).exists())
        self.assertEquals(content['results'][0]['snippets'],
                          Tags.objects.get(
                              slug=content['results'][0]['slug'])
                          .snippets_set.count())
        self.assertEquals(content['results'][0]['slug'],
                          Tags.objects.filter().order_by('-snippets')[0].slug)

    def test_tags_filtering(self):
        """
        Tag Filtering test
        """
        tag = Tags.objects.filter().order_by('?')[0]
        check_data = Tags.objects.filter(
            name__icontains=tag.name).order_by('-name')[:10]
        # match data
        serializer = TagsSerializer(instance=check_data, many=True)
        response = self.c.get(self.url, data={'ordering': '-name', self.key: 10,
                              'search': tag.name},
                              content_type='application/json')
        content = simplejson.loads(response.content)
        self.assertHttpOk(response)
        self.assertEquals(len(content['results']), check_data.count())
        self.assertEquals(content['results'], serializer.data)


class LanguagesViewTestCase(CommonTestMixin, HttpStatusCodeMixin, TestCase):
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
        Languages list
        """
        response = self.c.get(self.url, content_type='application/json')
        content = simplejson.loads(response.content)
        self.assertHttpOk(response)
        self.assertIsInstance(content, dict)
        self.assertIsInstance(content['results'], list)
        self.assertEquals(len(content['results']), self.limit)
        self.assertEquals(content['count'], Languages.objects.count())

    def test_languages_limit(self):
        """
        Check Tags per limit
        """
        response = self.c.get(self.url, data={self.key: 100},
                              content_type='application/json')
        content = simplejson.loads(response.content)
        self.assertHttpOk(response)
        self.assertEquals(content['count'], Languages.objects.count())
        self.assertGreater(len(content['results']), self.limit)
        self.assertIsInstance(content['results'], list)

    def test_languages_sort(self):
        """
        Key based Sort
        """
        # desc sorting
        response = self.c.get(self.url, content_type='application/json',
                              data={'ordering': '-pages', self.key: 1})
        content = simplejson.loads(response.content)
        self.assertHttpOk(response)
        self.assertEquals(content['count'], Languages.objects.count())
        self.assertIsInstance(content['results'], list)
        self.assertEquals(len(content['results']), 1)
        self.assertTrue(Languages.objects.filter(
            slug=content['results'][0]['slug']).exists())
        self.assertEquals(content['results'][0]['pages'],
                          Languages.objects.get(
                              slug=content['results'][0]['slug'])
                          .pages_set.count())
        self.assertEquals(content['results'][0]['slug'],
                          Languages.objects.filter().order_by('-pages')[0].slug)

    def test_language_filtering(self):
        """
        star orderd to the user's snippets
        """
        language = Languages.objects.filter().order_by('?')[0]
        check_data = Languages.objects.filter(
            name__icontains=language.name).order_by('-name')[:10]
        # match data
        serializer = LanguagesSerializer(instance=check_data, many=True)
        response = self.c.get(self.url, data={'ordering': '-name', self.key: 10,
                              'search': language.name},
                              content_type='application/json')
        content = simplejson.loads(response.content)
        self.assertHttpOk(response)
        self.assertEquals(len(content['results']), check_data.count())
        self.assertEquals(content['results'], serializer.data)


class TagSnippetsViewsTestCase(CommonTestMixin, HttpStatusCodeMixin, TestCase):
    """
    TagSnippetsViews TestCase
    """

    fixtures = ('initial_data', )

    def setUp(self):
        self.tag = Tags.objects.filter(snippets__isnull=False)[0]
        self.url = reverse('tag-snippets-list', args=[self.tag.slug])
        super(TagSnippetsViewsTestCase, self).setUp()

    def test_tag_snippets_list(self):
        """
        Tag Snippets list
        """
        response = self.c.get(self.url, content_type='application/json')
        content = simplejson.loads(response.content)
        self.assertHttpOk(response)
        self.assertEquals(content['count'], self.tag.snippets_set.count())
        self.assertGreaterEqual(len(content['results']),
                                self.tag.snippets_set.all()[:10].count())

    def test_invalid_tag(self):
        """
        Invalid tag can not be snippets
        """
        url = reverse('tag-snippets-list', args=['invalid-tag'])
        response = self.c.get(url, content_type='application/json')
        self.assertHttpNotFound(response)

    def test_tag_empty_snippets(self):
        self.tag.snippets_set.all().delete()
        response = self.c.get(self.url, content_type='application/json')
        content = simplejson.loads(response.content)
        self.assertEquals(content['count'], self.tag.snippets_set.count())
        self.assertGreaterEqual(len(content['results']), 0)


class LanguageSnippetsViewTestCase(CommonTestMixin, HttpStatusCodeMixin,
                                   TestCase):
    """
    LanguageSnippetsView TestCase
    """

    fixtures = ('initial_data', )

    def setUp(self):
        self.language = Languages.objects.filter(pages__isnull=False)[0]
        self.snippets = Snippets.objects.filter(
            pages__language__id=self.language.id)
        self.url = reverse('language-snippets-list', args=[self.language.slug])
        super(LanguageSnippetsViewTestCase, self).setUp()

    def test_language_snippets_list(self):
        response = self.c.get(self.url, content_type='application/json')
        content = simplejson.loads(response.content)
        self.assertHttpOk(response)
        self.assertEquals(content['count'], self.snippets.count())
        self.assertGreaterEqual(len(content['results']),
                                self.snippets[:10].count())

    def test_invalid_language(self):
        url = reverse('language-snippets-list', args=['invalid-tag'])
        response = self.c.get(url, content_type='application/json')
        self.assertHttpNotFound(response)


class SnippetsViewTestCase(CommonTestMixin, HttpStatusCodeMixin,
                           TestCase):
    """
    SnippetsView TestCase
    """

    fixtures = ('initial_data', )
    
    def setUp(self):
        self.url = reverse('snippets-list')
        self.user = User.objects.filter(snippets__isnull=True).order_by('?')[0]
        self.snippet = Snippets.objects.filter().order_by('?')[0]
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
        response = self.c.get(path=self.url, content_type='application/json')
        last_snippet = Snippets.objects.filter().order_by('-id')[0]
        content = simplejson.loads(response.content)
        self.assertHttpOk(response)
        self.assertEqual(len(content.get("results")),
                         Snippets.objects.filter()[:10].count())
        self.assertEqual(content.get("count"), Snippets.objects.all().count())
        self.assertEqual(content.get("results")[0]['slug'], last_snippet.slug)

    def test_create_snippet_not_authenticated(self):
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
        self.assertTrue(Snippets.objects.filter(slug=content['slug']).exists())
        self.assertTrue(Tags.objects.filter(
            name__in=self.data['tags']).exists())
        self.assertTrue(Snippets.objects.get(
            slug=content['slug']).pages_set.exists())


class SnippetDetailViewTestCase(CommonTestMixin, HttpStatusCodeMixin,
                                TestCase):
    """
    SnippetDetailView Test Cases
    """
    fixtures = ('initial_data', )

    def setUp(self):
        self.snippet = Snippets.objects.filter().order_by('?')[0]
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
        self.assertEqual(len(content['pages']), self.snippet.pages_set.count())
        self.assertEqual(content['public'], self.snippet.is_public)

    def test_invalid_snippet(self):
        url = reverse('snippets-detail', args=['invalid-tag'])
        response = self.c.get(url, content_type='application/json')
        self.assertHttpNotFound(response)

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
        self.assertEqual(Snippets.objects.get(id=self.snippet.id).name,
                         self.data['name'])

    def test_update_snippet_add_page(self):
        self.token_login(username=self.user.username, password='123456')
        count = self.snippet.pages_set.count()
        self.data['pages'].append({"content": "Hello World",
                                   "language": "javascript"})
        response = self.c.put(self.url, simplejson.dumps(self.data),
                              content_type='application/json',
                              **self.client_header)
        self.assertHttpOk(response)
        self.assertEqual(
            Snippets.objects.get(id=self.snippet.id).pages_set.count(), count+1)

    def test_update_not_authenticated(self):
        response = self.c.put(self.url, simplejson.dumps(self.data),
                              content_type='application/json',
                              **self.client_header)
        self.assertHttpUnauthorized(response)

    def test_destroy_snippet(self):
        self.token_login(username=self.user.username, password='123456')
        response = self.c.delete(self.url, content_type='application/json',
                                 **self.client_header)
        self.assertHttpNoContent(response)
        self.assertFalse(Snippets.objects.filter(id=self.snippet.id).exists())
