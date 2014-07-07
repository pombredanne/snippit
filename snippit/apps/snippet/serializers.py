# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Snippets
from account.serializers import UserDetailSerializer
from snippet.models import Tags, Languages, Pages, Comments


class BaseSnippetsSerializer(serializers.ModelSerializer):
    """
    Base Snippet Serializer
    """
    # author
    created_by = UserDetailSerializer(read_only=True)
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
        'created_at': '<date>', 'created_by': {'username': '<str>'...},
        'pages': '<int>'
    }

    """
    # snippet pages count
    pages = serializers.IntegerField(source='pages_set.count',
                                     read_only=True)

    class Meta:
        model = Snippets
        fields = ('name', 'slug', 'created_by', 'created_at', 'stars',
                  'comments', 'pages')


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
        'content': '<str>', 'snippet': {...}, 'language': {...}
    }
    """
    snippet = serializers.SlugField(source='snippet.slug')
    language = LanguagesSerializer()

    class Meta:
        model = Pages
        fields = ('content', 'snippet', 'language',)


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
        'name': '<str>', 'slug': '<str>', 'stars': '<int>',
        'created_at': '<date>', 'created_by': {'username': '<str>'...}
        'pages': [{...},], 'tags': [{...},]
    }
    """
    tags = TagsSerializer(many=True)
    pages = PagesSerializer(many=True, source='pages_set')

    class Meta:
        model = Snippets
        fields = ('name', 'slug', 'created_by', 'created_at', 'stars',
                  'comments', 'tags', 'pages', 'is_public')
        read_only_fields = ('slug',)