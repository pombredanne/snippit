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

    def validate_username(self, attrs, source):
        """
        username usage status
        """
        user = self.context['view'].request.user
        username = attrs.get('username')
        if isinstance(user, User) and user.username != username:
            if User.objects.filter(username=username).exists():
                raise serializers.ValidationError('username is used')
        return attrs

    def validate_email(self, attrs, source):
        """
        email usage status
        """
        user = self.context['view'].request.user
        email = attrs.get('email')
        if isinstance(user, User) and user.email != email:
            if User.objects.filter(username=email).exists():
                raise serializers.ValidationError('email is used')
        return attrs

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
    """
    email = serializers.EmailField(required=True)
    username = serializers.RegexField(
        required=True, regex=username_re,
        error_messages={'invalid': 'invalid username'})
    password = serializers.CharField(required=True, min_length=4)

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