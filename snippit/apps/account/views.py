# -*- coding: utf-8 -*-
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework import status
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
    serializer_class = UserDetailSerializer

    def get_queryset(self):
        user = self.get_object(queryset=self.queryset)
        followers = user.followers.all().values_list('follower__id', flat=True)
        return User.objects.filter(id__in=followers)

    def post(self, request, *args, **kwargs):
        user = self.get_object(self.queryset)
        follow = Follow.objects.create(following=user, follower=request.user)
        serializer = UserFollowSerializer(instance=follow)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def delete(self, request, *args, **kwargs):
        user = self.get_object(self.queryset)
        follow = Follow.objects.filter(follower=request.user, following=user)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
    filter_backends = (OrderingFilter,)
    lookup_field = "username"
    lookup_url_kwarg = "username"
    permission_classes = (AllowAny,)
    queryset = User.objects.filter(is_active=True)
    ordering_fields = ('stars', 'comments', 'name', 'created_at', )

    def get_queryset(self):
        user = self.get_object(queryset=self.queryset)
        return user.stars.filter(is_public=True)