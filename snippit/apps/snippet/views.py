from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from account.models import User
from api.generics import CreateDestroyAPIView
from .models import Tags, Languages
from .serializers import LanguagesSerializer, TagsSerializer
from rest_framework import permissions
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from snippet.models import Snippets
from snippet.permissions import (SnippetStarPermission,
                                 SnippetDestroyUpdatePermission)
from snippet.serializers import (ComprehensiveSnippetsSerializer,
                                 CommentsSerializer, SlimSnippetsSerializer)


class TagsView(generics.ListCreateAPIView):
    """
    Tags View

    Allowed Methods: ['GET', 'POST']
    Sample Data Type:
    {
        'name': '<str>'
    }
    Required Fields: ['name']
    """
    model = Tags
    serializer_class = TagsSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    filter_backends = (SearchFilter, OrderingFilter)
    # /api/tags/?search=<name>
    search_fields = ('name',)
    # ASC: /api/tags/?ordering=snippets
    # DESC: /api/tags/?ordering=-snippets
    ordering_fields = ('name', 'snippets')


class LanguagesView(generics.ListAPIView):
    """
    Languages View

    Allowed Methods: ['GET']
    """
    model = Languages
    serializer_class = LanguagesSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (SearchFilter, OrderingFilter)
    # /api/languages/?search=<name>
    search_fields = ('name',)
    # ASC: /api/languages/?ordering=pages
    # DESC: /api/languages/?ordering=-pages
    ordering_fields = ('name', 'pages')


class TagSnippetsViews(generics.ListAPIView):
    """
    Tag Snippets View

    Allowed Methods: ['GET']
    """
    model = Tags
    serializer_class = SlimSnippetsSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (SearchFilter, OrderingFilter)
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    # /api/tags/test/snippets/?search=<name>
    search_fields = ('name',)
    # ASC: /api/tags/test/snippets/?ordering=name
    # DESC: /api/tags/test/snippets/?ordering=-name
    ordering_fields = ('name', 'created_at')

    def get_queryset(self):
        tag = self.get_object(queryset=Tags.objects.all())
        return tag.snippets_set.filter(is_public=True)


class LanguageSnippetsView(generics.ListAPIView):
    """
    Language Snippets View

    Allowed Methods: ['GET']
    """
    model = Languages
    serializer_class = SlimSnippetsSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (SearchFilter, OrderingFilter)
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    # /api/tags/test/snippets/?search=<name>
    search_fields = ('name',)
    # ASC: /api/tags/test/snippets/?ordering=name
    # DESC: /api/tags/test/snippets/?ordering=-name
    ordering_fields = ('name', 'created_at')

    def get_queryset(self):
        language = self.get_object(queryset=Languages.objects.all())
        return Snippets.objects.filter(pages__language__id=language.id)


class SnippetsView(generics.ListCreateAPIView):
    """
    Snippets View

    Allowed Methods: ['GET', 'POST']
    """
    model = User
    serializer_class = ComprehensiveSnippetsSerializer
    filter_backends = (OrderingFilter,)
    lookup_field = "username"
    lookup_url_kwarg = "username"
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = User.objects.filter(is_active=True)
    ordering_fields = ('name', 'created_at', )

    def get_queryset(self):
        user = self.get_object(queryset=self.queryset)
        if self.request.user.username == user.username:
            return user.snippets_set.all()
        return user.snippets_set.filter(is_public=True)

    def pre_save(self, obj):
        user = self.get_object(queryset=self.queryset)
        obj.created_by = user


class SnippetDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Snippet Detail View

    Allowed Methods: ['GET', 'PUT', 'DELETE']
    """
    model = User
    serializer_class = ComprehensiveSnippetsSerializer
    lookup_field = "username"
    lookup_url_kwarg = "username"
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          SnippetDestroyUpdatePermission)
    queryset = User.objects.filter(is_active=True)

    def get_object(self, queryset=None):
        user = super(SnippetDetailView, self).get_object(queryset=self.queryset)
        snippet = get_object_or_404(Snippets, created_by=user,
                                    slug=self.kwargs.get('slug'))
        return snippet


class SnippetStarView(CreateDestroyAPIView):
    """
    Snippet star/unstar

    Allowed Methods: ['POST', 'DELETE']
    """
    model = User
    serializer_class = ComprehensiveSnippetsSerializer
    lookup_field = "username"
    lookup_url_kwarg = "username"
    permission_classes = (permissions.IsAuthenticated, SnippetStarPermission)
    queryset = User.objects.filter(is_active=True)

    def get_object(self, queryset=None):
        user = super(SnippetStarView, self).get_object(queryset=self.queryset)
        snippet = get_object_or_404(Snippets, created_by=user,
                                    slug=self.kwargs.get('slug'))
        return snippet

    def post(self, request, *args, **kwargs):
        snippet = self.get_object()
        user = request.user
        user.stars.add(snippet)
        serializer = self.serializer_class(instance=snippet)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def delete(self, request, *args, **kwargs):
        snippet = self.get_object()
        user = request.user
        user.stars.remove(snippet)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SnippetCommentsView(generics.ListCreateAPIView):
    """
    Snippet Comments View

    Allowed Methods: ['GET', 'POST']
    """
    model = User
    serializer_class = CommentsSerializer
    filter_backends = (OrderingFilter,)
    lookup_field = "username"
    lookup_url_kwarg = "username"
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    ordering_fields = ('created_at', )
    queryset = User.objects.filter(is_active=True)

    def get_queryset(self):
        user = self.get_object(queryset=self.queryset)
        snippet = get_object_or_404(Snippets, created_by=user,
                                    slug=self.kwargs.get('slug'))
        return snippet.comments_set.all()

    def pre_save(self, obj):
        user = self.get_object(queryset=self.queryset)
        snippet = get_object_or_404(Snippets, created_by=user,
                                    slug=self.kwargs.get('slug'))
        obj.created_by = self.get_object(queryset=self.queryset)
        obj.snippet = snippet