# -*- coding: utf-8 -*-
import simplejson

from django.test import TestCase
from snippet.models import Tags
from snippet.serializers import TagsSerializer
from snippit.core.mixins import CommonTestMixin, HttpStatusCodeMixin
from django.core.urlresolvers import reverse
from django.conf import settings


class TagsViewTest(CommonTestMixin, HttpStatusCodeMixin, TestCase):
    """
    TagsView Test Cases
    """
    fixtures = ('initial_data', )

    def test_tags_list(self):
        """
        Tags list
        """
        limit = settings.REST_FRAMEWORK['PAGINATE_BY']
        url = reverse('tags-list')
        response = self.c.get(url)
        content = simplejson.loads(response.content)
        self.assertHttpOk(response)
        self.assertIsInstance(content, dict)
        self.assertIsInstance(content['results'], list)
        self.assertEquals(len(content['results']), limit)
        self.assertEquals(content['count'], Tags.objects.count())

    def test_tags_limit(self):
        """
        Check Tags per limit
        """
        limit = settings.REST_FRAMEWORK['PAGINATE_BY']
        key = settings.REST_FRAMEWORK['PAGINATE_BY_PARAM']
        url = reverse('tags-list')
        response = self.c.get(url, data={key: 100})
        content = simplejson.loads(response.content)
        self.assertHttpOk(response)
        self.assertEquals(content['count'], Tags.objects.count())
        self.assertGreater(len(content['results']), limit)
        self.assertIsInstance(content['results'], list)

    def test_tags_sort(self):
        """
        Key based Sort
        """
        url = reverse('tags-list')
        key = settings.REST_FRAMEWORK['PAGINATE_BY_PARAM']
        # desc sorting
        response = self.c.get(url, data={'ordering': '-snippets', key: 1})
        content = simplejson.loads(response.content)
        self.assertHttpOk(response)
        self.assertEquals(content['count'], Tags.objects.count())
        self.assertIsInstance(content['results'], list)
        self.assertEquals(len(content['results']), 1)
        self.assertTrue(Tags.objects.filter(
            slug=content['results'][0]['slug']).exists())
        self.assertEquals(content['results'][0]['snippets'],
                          Tags.objects.get(
                              slug=content['results'][0]['slug']
                          ).snippets_set.count())

    def test_tags_filtering(self):
        """
        Tag Filtering test
        """
        url = reverse('tags-list')
        key = settings.REST_FRAMEWORK['PAGINATE_BY_PARAM']
        tag = Tags.objects.filter().order_by('?')[0]
        check_data = Tags.objects.filter(
            name__icontains=tag.name).order_by('-name')[:10]
        # match data
        serializer = TagsSerializer(instance=check_data, many=True)
        response = self.c.get(url, data={'ordering': '-name', key: 10,
                                         'search': tag.name})
        content = simplejson.loads(response.content)
        self.assertHttpOk(response)
        self.assertEquals(content['count'], check_data.count())
        self.assertEquals(content['results'], serializer.data)