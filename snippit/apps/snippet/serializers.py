# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Snippets
from account.serializers import UserDetailSerializer
from snippet.models import Tags, Languages


class SlimSnippetsSerializer(serializers.ModelSerializer):
    """
    Snippets Serializer for User Stars

    {
        'name': '<str>', 'slug': '<str>', 'stars': '<int>',
        'created_at': '<date>', 'created_by': {'username': '<str>'...}
    }

    """
    created_by = UserDetailSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True,
                                           format='%d-%m-%Y %H:%M',)
    stars = serializers.IntegerField(source='user_set.count')
    comments = serializers.IntegerField(source='comments_set.count')

    class Meta:
        model = Snippets
        fields = ('name', 'slug', 'created_by', 'created_at', 'stars',
                  'comments')


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