# -*- coding: utf-8 -*-
from account.models import User
from rest_framework import serializers


class UserDetailSerializer(serializers.ModelSerializer):
    """
    User Detail, User Profile Update Serializer

    {
      'username': '<str>', 'email': '<str>', 'first_name': '<str>',
      'last_name': '<str>', 'location': '<str>', 'website': '<str>',
      'created_at': '<datetime>', 'followers': '<int>' 'followings': '<int>'
    }
    """

    followers = serializers.SerializerMethodField('followers_count')
    followings = serializers.SerializerMethodField('followings_count')
    created_at = serializers.DateTimeField(read_only=True,
                                           format='%d-%m-%Y %H:%M',)

    def followers_count(self, obj):
        """
        User Followers Count
        """
        return obj.following.count()

    def followings_count(self, obj):
        """
        User Followings Count
        """
        return obj.followers.count()

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'location',
                  'website', 'created_at', 'followers', 'followings')