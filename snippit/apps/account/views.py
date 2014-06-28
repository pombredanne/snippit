# -*- coding: utf-8 -*-
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from account.models import User
from .serializers import UserRegisterSerializer


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