from rest_framework import generics
from .models import Tags, Languages
from .serializers import LanguagesSerializer, TagsSerializer
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter


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
    permission_classes = (IsAuthenticatedOrReadOnly, )
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
    permission_classes = (AllowAny,)
    filter_backends = (SearchFilter, OrderingFilter)
    # /api/languages/?search=<name>
    search_fields = ('name',)
    # ASC: /api/languages/?ordering=pages
    # DESC: /api/languages/?ordering=-pages
    ordering_fields = ('name', 'pages')