# -*- coding: utf-8 -*-
from account.models import User
from rest_framework import serializers
from .validators import username_re


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


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    User Register Serializer
    """
    email = serializers.EmailField(required=True)
    username = serializers.RegexField(
        required=True, regex=username_re,
        error_messages={'invalid': 'invalid username'})
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def validate_username(self, attrs, source):
        """
        username usage status
        """
        username = attrs.get('username')
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError('username this already exists')
        return attrs

    def validate_email(self, attrs, source):
        """
        email usage status
        """
        email = attrs.get('email', None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('E-Mail this already exists')
        return attrs

    def restore_object(self, attrs, instance=None):
        instance = super(UserRegisterSerializer, self).\
            restore_object(attrs, instance)
        self.fields.pop('password')
        return instance