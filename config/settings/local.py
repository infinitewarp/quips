# -*- coding: utf-8 -*-
"""
Local settings overrides.

- Run in Debug mode
- Add django-extensions as app
"""

from .common import *  # noqa: F403
# ruff: noqa: F405

# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", default=True)
TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["*"])

# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY", default="local")

CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS += ("django_extensions",)

TEST_RUNNER = "django.test.runner.DiscoverRunner"
