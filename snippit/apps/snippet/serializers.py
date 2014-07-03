# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import Snippets
from account.serializers import UserDetailSerializer


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

    class Meta:
        model = Snippets
        fields = ('name', 'slug', 'created_by', 'created_at', 'stars')