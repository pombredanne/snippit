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

    Unique Fields: ['username', 'email']
    """

    followers = serializers.IntegerField(source='following.count',
                                         read_only=True)
    followings = serializers.IntegerField(source='followers.count',
                                          read_only=True)
    created_at = serializers.DateTimeField(read_only=True,
                                           format='%d-%m-%Y %H:%M',)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'location',
                  'website', 'created_at', 'followers', 'followings')


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    User Register Serializer

    {
        'username': '<str>', 'email': '<str>'
    }

    Unique Fields: ['username', 'email']
    """
    email = serializers.EmailField(required=True)
    username = serializers.RegexField(
        required=True, regex=username_re,
        error_messages={'invalid': 'invalid username'})
    password = serializers.CharField(required=True, min_length=4)

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def restore_object(self, attrs, instance=None):
        """
        Instantiate a new User instance.
        """
        assert instance is None, 'Cannot update users ' \
                                 'with UserRegisterSerializer'
        user = User(email=attrs['email'], username=attrs['username'])
        user.set_password(attrs['password'])
        # visible password
        self.fields.pop('password')
        return user