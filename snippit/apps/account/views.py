# -*- coding: utf-8 -*-
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from account.models import User
from .serializers import UserRegisterSerializer, UserDetailSerializer
from .permissions import UserUpdatePermission


class UserRegisterView(CreateAPIView):
    """
    User Register View

    Allowed Methods: ['POST']
    Sample Data Type:
    {
        'username': '<str>', 'email': '<str>', 'password': '<str>'
    }
    """
    model = User
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)


class UserDetailView(RetrieveUpdateAPIView):
    """
    User Detail View

    Allowed Methods: ['PUT', 'GET']
    Sample Data Type:
    {
        "username": "<str>", "email": "<str>",
        "first_name": "<str>", "last_name": "<str>",
        "location": "<str>", "website": "<str>"
    }
    """
    permission_classes = (UserUpdatePermission,)
    serializer_class = UserDetailSerializer
    model = User
    queryset = User.objects.filter(is_active=True)
    lookup_field = "username"
    lookup_url_kwarg = "username"