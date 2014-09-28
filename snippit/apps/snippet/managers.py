from django.db.models import Manager


class SnippetsManager(Manager):
    def optimized(self):
        queryset = self.get_queryset()
        return queryset.select_related('created_by') \
            .prefetch_related('tag', 'created_by__following',
                              'created_by__followers',
                              'created_by__stars',
                              'comment_set',
                              'page_set',
                              'page_set__language').filter()

    def public(self):
        return self.get_queryset().filter(is_public=True)

    def private(self):
        return self.get_queryset().filter(is_public=False)
