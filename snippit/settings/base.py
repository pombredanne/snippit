"""
Django settings for snippit project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
APPS = os.path.join(BASE_DIR, 'apps')
sys.path.insert(1, APPS)
sys.path.insert(2, BASE_DIR)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '56#z0uc5v%p-60az6s4pm3wxajt5u9*cfe4m12v+6&iqvzpfxi'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

import djcelery
djcelery.setup_loader()

BROKER_URL = 'amqp://guest:guest@localhost:5672//'

# Application definition
DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
    'south',
    'django_nose',
    'djcelery',
    'djcelery_email'
)

LOCAL_APPS = (
    'account',
    'api',
    'auth',
    'snippet',
)

EMAIL_BACKEND = 'djcelery_email.backends.CeleryEmailBackend'

CELERY_EMAIL_TASK_CONFIG = {
    'name': 'email_send',
    'ignore_result': True,
}

CELERY_IMPORTS = ('djcelery_email.tasks', )

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

FIXTURE_DIRS = (
    os.path.join(APPS, '/account/fixtures/'),
    os.path.join(APPS, '/snippet/fixtures/')
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'snippit.urls'

WSGI_APPLICATION = 'snippit.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates')
)
# END TEMPLATE CONFIGURATION

AUTH_USER_MODEL = 'account.User'
ALLOWED_HOSTS = ["*"]


APPEND_SLASH = False


# MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = os.path.normpath(os.path.join(BASE_DIR, 'media'))
MEDIA_URL = '/media/'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

SOUTH_TESTS_MIGRATE = False

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = os.path.normpath(os.path.join(BASE_DIR, 'static'))
STATIC_URL = '/static/'


# See: https://docs.djangoproject.com/en/dev/ref/contrib
#       /staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
# END STATIC FILE CONFIGURATION

# Rest Framework Config http://django-rest-framework.org/#installation
REST_FRAMEWORK = {
    # Use hyperlinked styles by default.
    # Only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.ModelSerializer',
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'auth.authentication.ExpiringTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    # Custom Exception Handler
    'EXCEPTION_HANDLER': 'api.exceptions.custom_exception_handler',

    'TEST_REQUEST_RENDERER_CLASSES': (
        'rest_framework.renderers.MultiPartRenderer',
        'rest_framework.renderers.JSONRenderer',
    ),
    # Pagination settings
    'PAGINATE_BY': 10,
    'PAGINATE_BY_PARAM': 'page_size',
    'MAX_PAGINATE_BY': 100,
}

# Api Token Expire: 15 days
API_TOKEN_TTL = 15

# Gravatar settings
GRAVATAR = {
    'base_url': 'https://secure.gravatar.com/avatar/',
    'default_avatar': '',
    'size': 130
}

NOTIFICATION_FROM_EMAIL = 'noreply@snippit.in'

# mail notification
MAIL_NOTIFICATION = {
    'welcome_email': {
        'subject': 'Welcome %s',
        'template': 'mail/welcome.html'
    },
    'add_comment': {
        'subject': '%s snippet comment added',
        'template': 'mail/add_comment.html'
    },
    'follow': {
        'subject': '%s, you have a new follower on Snippit!',
        'template': 'mail/follow.html'
    }
}

try:
    from local import *
except ImportError:
    pass
