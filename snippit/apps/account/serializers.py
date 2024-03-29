# -*- coding: utf-8 -*-
from account.models import User, Follow
from rest_framework import serializers
from .validators import username_re
from .fields import GravatarField


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
    avatar = GravatarField(source='email')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'location',
                  'website', 'created_at', 'followers', 'followings', 'avatar')


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


class UserFollowSerializer(serializers.ModelSerializer):
    """
    UserFollowSerializer
    Return new data after saving a Follow object

    {
        following: {'username': '<str>', 'email': '<str>' ...}
        follower: {'username': '<str>', 'email': '<str>' ...}
    }
    """

    following = UserDetailSerializer(read_only=True)
    follower = UserDetailSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ('following', 'follower')


class UserChangePasswordSerializer(serializers.ModelSerializer):
    """
    Account New Password
    """
    # existing password
    password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('password', 'new_password', 'confirm_password')

    def validate(self, attrs):
        new_password = attrs.get('new_password', None)
        confirm_password = attrs.get('confirm_password', None)
        if not new_password or not confirm_password:
            raise serializers.ValidationError('passwords did not match')
        if not new_password == confirm_password:
            raise serializers.ValidationError('passwords did not match')
        return attrs

    def validate_password(self, attrs, source):
        password = attrs.get('password')
        # user object
        user = self.object
        if not user.check_password(password):
            raise serializers.ValidationError('passwords invalid')
        return attrs

    def restore_object(self, attrs, instance=None):
        instance = super(UserChangePasswordSerializer, self).restore_object(
            attrs, instance)
        instance.set_password(attrs.get('new_password'))
        # change response fields
        self.fields = UserDetailSerializer(instance=instance).fields
        return instance
