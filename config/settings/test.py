# -*- coding: utf-8 -*-
"""
Test settings

- Use sqlite for database
"""

from .common import *  # noqa: F403
# ruff: noqa: F405

# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", default=False)
TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG

# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY", default="test")

CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

DATABASES["default"] = env.db(default="sqlite:////db.sqlite3")
DATABASES["default"]["ATOMIC_REQUESTS"] = True

TEST_RUNNER = "django.test.runner.DiscoverRunner"
