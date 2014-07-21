# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Snippets, Tags, Languages, Pages, Comments
from account.serializers import UserDetailSerializer
from .fields import SerializerRelatedField, GetOrCreateField


class BaseSnippetsSerializer(serializers.HyperlinkedModelSerializer):
    """
    Base Snippet Serializer
    """
    url = serializers.HyperlinkedIdentityField(view_name='snippets-detail',
                                               lookup_field='slug')
    comments_url = serializers.HyperlinkedIdentityField(
        view_name='snippets-comments', lookup_field='slug')
    star_url = serializers.HyperlinkedIdentityField(
        view_name='snippets-star', lookup_field='slug')
    # author
    owner = UserDetailSerializer(read_only=True, source='created_by')
    created_at = serializers.DateTimeField(read_only=True,
                                           format='%d-%m-%Y %H:%M',)
    # starred count
    stars = serializers.IntegerField(source='user_set.count', read_only=True)
    # comments count
    comments = serializers.IntegerField(source='comments_set.count',
                                        read_only=True)

    class Meta:
        abstract = True


class SlimSnippetsSerializer(BaseSnippetsSerializer):
    """
    Snippets Serializer for User Stars

    {
        'name': '<str>', 'slug': '<str>', 'stars': '<int>',
        'created_at': '<date>', 'owner': {'username': '<str>'...},
        'pages': '<int>', 'url': '<str>',
        'comments_url': '<str>', 'star_url': '<str>'
    }

    """
    # snippet pages count
    pages = serializers.IntegerField(source='pages_set.count',
                                     read_only=True)

    class Meta:
        model = Snippets
        fields = ('name', 'slug', 'owner', 'created_at', 'stars',
                  'comments', 'pages', 'url', 'comments_url', 'star_url')


class TagsSerializer(serializers.ModelSerializer):
    """
    Tag Model Serializer

    {
        'name': '<str>', 'slug': '<str>', 'snippets': '<int>'
    }
    """
    snippets = serializers.IntegerField(source='snippets_set.count',
                                        read_only=True)

    class Meta:
        model = Tags
        fields = ('name', 'slug', 'snippets')
        read_only_fields = ('slug',)


class LanguagesSerializer(serializers.ModelSerializer):
    """
    Language Model Serializer

    {
        'name': '<str>', 'slug': '<str>', 'pages': '<int>'
    }
    """
    pages = serializers.IntegerField(source='pages_set.count', read_only=True)

    class Meta:
        model = Languages
        fields = ('name', 'slug', 'pages')
        read_only_fields = ('slug',)


class PagesSerializer(serializers.ModelSerializer):
    """
    Pages Model Serializer

    {
        'content': '<str>', 'language': {...}
    }
    """
    language = SerializerRelatedField(slug_field='slug',
                                      serializer_field=LanguagesSerializer)

    class Meta:
        model = Pages
        fields = ('content', 'language',)


class CommentsSerializer(serializers.ModelSerializer):
    """
    Comments Model Serializer

    {
        'author': {...}, 'snippet': {...}, 'created_at': '<data>',
        'comment': '<str>'
    }
    """

    author = UserDetailSerializer(read_only=True)
    snippet = SlimSnippetsSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True,
                                           format='%d-%m-%Y %H:%M',)

    class Meta:
        model = Comments
        fields = ('author', 'snippet', 'comment', 'created_at',)


class ComprehensiveSnippetsSerializer(BaseSnippetsSerializer):
    """
    Comprehensive Snippets Serializer

    {
        'url': '<str>', 'name': '<str>', 'slug': '<str>', 'stars': '<int>',
        'created_at': '<date>', 'owner': {'username': '<str>'...}
        'pages': [{...},], 'tags': [{...}],
        'public': <bool>, 'comments_url': '<str>', 'star_url': '<str>'
    }
    """
    tags = GetOrCreateField(many=True, serializer_field=TagsSerializer,
                            required=False, slug_field='name')
    pages = PagesSerializer(many=True, source='pages_set',
                            allow_add_remove=True)
    public = serializers.BooleanField(source='is_public', required=True)

    class Meta:
        model = Snippets
        fields = ('url', 'comments_url', 'star_url', 'name', 'slug', 'owner',
                  'created_at', 'stars', 'comments', 'tags', 'pages', 'public',)
        read_only_fields = ('slug',)
