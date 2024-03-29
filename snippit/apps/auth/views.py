# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.utils.timezone import utc
from django.contrib.auth import login, logout
from rest_framework.authtoken.views import ObtainAuthToken
from account.models import User
from account.serializers import UserDetailSerializer
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.conf import settings


class SessionAuthenticationView(APIView):
    """
    Session ObtainAuthToken View
    """
    serializer_class = AuthTokenSerializer
    permission_classes = (AllowAny,)
    queryset = User.objects.filter(is_active=True)

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
    queryset = User.objects.filter(is_active=True)

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class TokenAuthenticationView(ObtainAuthToken):
    """
    Simple token based authentication.
    """
    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            token, created = self.model.objects.get_or_create(
                user=serializer.object['user'])

            utc_now = datetime.utcnow().replace(tzinfo=utc)
            key = token.key
            # change expired token
            if token.created < (utc_now - timedelta(
                    days=settings.API_TOKEN_TTL)):
                key = token.generate_key()
            # set last auth. date
            if not created:
                self.model.objects.filter(key=token.key)\
                                  .update(key=key, created=utc_now)
            user_data = UserDetailSerializer(serializer.object['user'])
            expiration_date = utc_now + timedelta(days=settings.API_TOKEN_TTL)
            return Response({'user': user_data.data, 'token': key,
                             'expiration_date': expiration_date})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenLogoutView(APIView):
    """
    Token Logout View
    """
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.filter(is_active=True)

    def post(self, request):
        auth = request.auth
        auth.delete()
        return Response(status=status.HTTP_200_OK)
