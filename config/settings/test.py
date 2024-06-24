# -*- coding: utf-8 -*-
"""
Test settings

- Use sqlite for database
"""

from .common import *  # noqa: F403
# ruff: noqa: F405

DEBUG = env.bool("DJANGO_DEBUG", default=False)
TEMPLATES[0]["OPTIONS"]["debug"] = DEBUG

SECRET_KEY = env("DJANGO_SECRET_KEY", default="test")

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "",
    }
}

DATABASES["default"] = env.db(default="sqlite:////db.sqlite3")
DATABASES["default"]["ATOMIC_REQUESTS"] = True

TEST_RUNNER = "django.test.runner.DiscoverRunner"
