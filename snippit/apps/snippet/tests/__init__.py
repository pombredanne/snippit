from .models import (
    CommentsTestCase, LanguageTestCase, SnippetsTestCase, TagsTestCase,
    PagesTestCase
)
from .serializers import (
    SlimSnippetsSerializerTestCase, LanguagesSerializerTestCase,
    CommentsSerializerTestCase, ComprehensiveSnippetsSerializerTestCase,
    TagsSerializerTestCase, PagesSerializerTestCase,
)

from .views import (TagsViewTestCase, LanguagesViewTestCase,
                    TagSnippetsViewsTestCase, LanguageSnippetsViewTestCase)