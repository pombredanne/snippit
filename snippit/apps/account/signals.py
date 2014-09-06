import django.dispatch

welcome_email = django.dispatch.Signal(providing_args=['user'])

follow_done = django.dispatch.Signal(providing_args=['user'])
