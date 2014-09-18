# -*- coding: utf-8 -*-
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from account.serializers import UserChangePasswordSerializer
from account.signals import welcome_email, follow_done
from .models import User, Follow
from api.generics import ListCreateDestroyAPIView
from .serializers import (UserRegisterSerializer, UserDetailSerializer,
                          UserFollowSerializer)
from .permissions import UserUpdatePermission, UserFollowPermission
from snippet.serializers import (SlimSnippetsSerializer,
                                 ComprehensiveSnippetsSerializer)


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
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)

    def post_save(self, obj, created=False):
        welcome_email.send(sender=self, user=obj)


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
    # inactive user cannot update and view
    queryset = User.objects.filter(is_active=True)
    # db field
    lookup_field = "username"
    # url field /api/account/<username>/
    lookup_url_kwarg = "username"


class UserChangePasswordView(generics.UpdateAPIView):
    """
    User Change Password View

    Allowed Methods: ['PUT', 'PATCH']
    """
    queryset = User.objects.filter(is_active=True)
    permission_classes = (UserUpdatePermission,)
    serializer_class = UserChangePasswordSerializer
    lookup_field = "username"
    lookup_url_kwarg = "username"


class UserFollowersView(ListCreateDestroyAPIView):
    """
    User Followers List and User Follow/Unfollow process

    Allowed Methods: ['POST', 'GET', 'DELETE']
    """
    permission_classes = (IsAuthenticatedOrReadOnly, UserFollowPermission,)
    lookup_field = "username"
    lookup_url_kwarg = "username"
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserDetailSerializer

    def get_queryset(self):
        user = self.get_object(queryset=self.queryset)
        return user.get_followers()

    def post(self, request, *args, **kwargs):
        user = self.get_object(self.queryset)
        follow = Follow.objects.create(following=user, follower=request.user)
        serializer = UserFollowSerializer(instance=follow)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def post_save(self, obj, created=False):
        follow_done.send(sender=self, follow=obj)

    def delete(self, request, *args, **kwargs):
        user = self.get_object(self.queryset)
        user.followers.filter(follower=request.user).delete()
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
    queryset = User.objects.filter(is_active=True)

    def get_queryset(self):
        user = self.get_object(queryset=self.queryset)
        return user.get_followings()


class UserStarredSnippetsView(generics.ListAPIView):
    """
    User Starred Snippets

    Allowed Methods: ['GET']
    """
    serializer_class = SlimSnippetsSerializer
    filter_backends = (OrderingFilter,)
    lookup_field = "username"
    lookup_url_kwarg = "username"
    permission_classes = (AllowAny,)
    queryset = User.objects.filter(is_active=True)
    ordering_fields = ('stars', 'comments', 'name', 'created_at', )

    def get_queryset(self):
        user = self.get_object(queryset=self.queryset)
        return user.stars.optimized().filter(is_public=True)


class UserSnippetsView(generics.ListAPIView):
    """
    user Added Snippets View

    Allowed Methods: ['GET']
    """
    serializer_class = ComprehensiveSnippetsSerializer
    filter_backends = (OrderingFilter,)
    lookup_field = "username"
    lookup_url_kwarg = "username"
    permission_classes = (AllowAny,)
    queryset = User.objects.filter(is_active=True)
    ordering_fields = ('name', 'created_at', )

    def get_queryset(self):
        user = self.get_object(queryset=self.queryset)
        if self.request.user.username == user.username:
            return user.snippets_set.all()
        return user.snippets_set.optimized().filter(is_public=True)
