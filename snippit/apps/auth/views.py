# -*- coding: utf-8 -*-
from django.contrib.auth import login, logout
from account.models import User
from account.serializers import UserDetailSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status


class SessionAuthenticationView(APIView):
    """
    Session ObtainAuthToken View
    """
    serializer_class = AuthTokenSerializer
    permission_classes = (AllowAny,)
    model = User

    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            login(request, serializer.object['user'])
            user_data = UserDetailSerializer(serializer.object['user'])
            return Response(user_data.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SessionLogoutView(APIView):
    """
    Session Logout View
    """
    permission_classes = (IsAuthenticated,)
    model = User

    def get(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class TokenLogoutView(APIView):
    """
    Token Logout View
    """
    permission_classes = (IsAuthenticated,)
    model = User

    def get(self, request):
        auth = request.auth
        auth.delete()
        return Response(status=status.HTTP_200_OK)