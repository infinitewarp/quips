# -*- coding: utf-8 -*-
"""
Test settings

- Use console backend for emails
- Use sqlite for database
"""

from .common import *  # noqa

DEBUG = env.bool('DJANGO_DEBUG', default=False)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND',
                    default='django.core.mail.backends.console.EmailBackend')

SECRET_KEY = env('DJANGO_SECRET_KEY', default='test')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

DATABASES['default'] = env.db(default='sqlite:////db.sqlite3')
DATABASES['default']['ATOMIC_REQUESTS'] = True

TEST_RUNNER = 'django.test.runner.DiscoverRunner'
