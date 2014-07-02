# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from .models import User, Follow
from api.generics import ListCreateDestroyAPIView
from .serializers import (UserRegisterSerializer, UserDetailSerializer,
                          UserFollowSerializer)
from .permissions import UserUpdatePermission, UserFollowPermission
from snippet.serializers import SlimSnippetsSerializer


class UserRegisterView(generics.CreateAPIView):
    """
    User Register View

    Allowed Methods: ['POST']
    Sample Data Type:
    {
        'username': '<str>', 'email': '<str>', 'password': '<str>'
    }
    Required Fields: ['username', 'email', 'password']
    """
    model = User
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)


class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    User Detail View

    Allowed Methods: ['PUT', 'GET', 'PATCH']
    Sample Data Type:
    {
        "username": "<str>", "email": "<str>",
        "first_name": "<str>", "last_name": "<str>",
        "location": "<str>", "website": "<str>"
    }
    Required Fields: ['username', 'email']
    """
    permission_classes = (UserUpdatePermission,)
    serializer_class = UserDetailSerializer
    model = User
    # inactive user cannot update and view
    queryset = User.objects.filter(is_active=True)
    # db field
    lookup_field = "username"
    # url field /api/account/<username>/
    lookup_url_kwarg = "username"


class UserFollowersView(ListCreateDestroyAPIView):
    """
    User Followers List and User Follow/Unfollow process

    Allowed Methods: ['POST', 'GET', 'DELETE']
    """
    permission_classes = (IsAuthenticatedOrReadOnly, UserFollowPermission,)
    slug_field = "username"
    slug_url_kwarg = "username"
    model = User
    queryset = User.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'DELETE'):
            return UserFollowSerializer
        return UserDetailSerializer

    def get_queryset(self):
        user = self.get_object(queryset=self.queryset)
        followers = user.followers.all().values_list('follower__id', flat=True)
        return User.objects.filter(id__in=followers)

    def pre_save(self, obj):
        # Calling before saving a Follow object.
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        obj.following = user
        obj.follower = self.request.user

    def filter_queryset(self, queryset):
        if self.request.method in ('POST', 'DELETE'):
            username = self.kwargs.get('username')
            user = get_object_or_404(User, username=username)
            # change db field queryset.filter(following__username=username)
            self.slug_field = 'following__username'
            # change queryset
            return Follow.objects.filter(follower=self.request.user,
                                         following=user)
        return queryset


class UserFollowingsView(ListCreateDestroyAPIView):
    """
    User Followings

    Allowed Methods: ['GET']
    """
    permission_classes = (AllowAny,)
    serializer_class = UserDetailSerializer
    lookup_field = "username"
    lookup_url_kwarg = "username"
    model = User
    queryset = User.objects.filter(is_active=True)

    def get_queryset(self):
        user = self.get_object(queryset=self.queryset)
        followers = user.following.all().values_list('following__id', flat=True)
        return User.objects.filter(id__in=followers, is_active=True)


class UserStarredSnippetsView(generics.ListAPIView):
    """
    User Starred Snippets

    Allowed Methods: ['GET']
    """
    model = User
    serializer_class = SlimSnippetsSerializer
    lookup_field = "username"
    lookup_url_kwarg = "username"
    permission_classes = (AllowAny,)
    queryset = User.objects.filter(is_active=True)

    def get_queryset(self):
        user = self.get_object(queryset=self.queryset)
        return user.stars.filter(is_public=True)