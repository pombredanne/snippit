from rest_framework.response import Response
from account.models import User
from account.serializers import UserDetailSerializer
from api.generics import ListCreateDestroyAPIView
from .models import Tags, Languages, Snippets
from rest_framework import permissions, status, generics
from rest_framework.filters import SearchFilter, OrderingFilter
from .permissions import SnippetStarPermission, SnippetDestroyUpdatePermission
from snippet import serializers


class TagsView(generics.ListAPIView):
    """
    Tags View

    Allowed Methods: ['GET']
    """
    model = Tags
    serializer_class = serializers.TagsSerializer
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
    serializer_class = serializers.LanguagesSerializer
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
    serializer_class = serializers.SlimSnippetsSerializer
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
    serializer_class = serializers.SlimSnippetsSerializer
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
    serializer_class = serializers.ComprehensiveSnippetsSerializer
    filter_backends = (OrderingFilter,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Snippets.objects.filter(is_public=True).order_by('-id')
    ordering_fields = ('name', 'created_at', )

    def pre_save(self, obj):
        user = self.request.user
        obj.created_by = user


class SnippetDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Snippet Detail View

    Allowed Methods: ['GET', 'PUT', 'DELETE']
    """
    model = Snippets
    serializer_class = serializers.ComprehensiveSnippetsSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          SnippetDestroyUpdatePermission)


class SnippetStarView(ListCreateDestroyAPIView):
    """
    Snippet star/unstar

    Allowed Methods: ['POST', 'DELETE']
    """
    model = Snippets
    serializer_class = serializers.ComprehensiveSnippetsSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    permission_classes = (permissions.IsAuthenticated, SnippetStarPermission)
    queryset = Snippets.objects.all()

    def post(self, request, *args, **kwargs):
        snippet = self.get_object()
        user = request.user
        user.stars.add(snippet)
        serializer = self.serializer_class(instance=snippet,
                                           context={'request': request})
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def delete(self, request, *args, **kwargs):
        snippet = self.get_object()
        user = request.user
        user.stars.remove(snippet)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get(self, request, *args, **kwargs):
        # Check if a snippet is starred
        snippet = self.get_object()
        if request.user.stars.filter(id=snippet.id).exists():
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_200_OK)


class SnippetCommentsView(generics.ListCreateAPIView):
    """
    Snippet Comments View

    Allowed Methods: ['GET', 'POST']
    """
    model = Snippets
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    serializer_class = serializers.CommentsSerializer
    filter_backends = (OrderingFilter,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    ordering_fields = ('created_at', )
    queryset = Snippets.objects.all()

    def get_queryset(self):
        snippet = self.get_object(queryset=self.queryset)
        return snippet.comments_set.all()

    def pre_save(self, obj):
        snippet = self.get_object(queryset=self.queryset)
        obj.author = self.request.user
        obj.snippet = snippet


class SnippetStarredUsersView(generics.ListAPIView):
    """
    Snippet Starred Users View
    """
    model = Snippets
    lookup_field = "slug"
    lookup_url_kwarg = "slug"
    serializer_class = UserDetailSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Snippets.objects.all()
    ordering_fields = ('username', 'first_name', 'last_name')

    def get_queryset(self):
        snippet = self.get_object(queryset=self.queryset)
        return snippet.user_set.all()
