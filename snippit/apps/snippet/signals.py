import django.dispatch

snippet_add_comment = django.dispatch.Signal(
    providing_args=['snippet', 'comment'])
