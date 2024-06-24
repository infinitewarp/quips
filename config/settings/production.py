# -*- coding: utf-8 -*-
"""
Production settings overrides.

- Set appropriate secrets, security, host, etc.
- Use Redis cache.
"""

from __future__ import absolute_import, unicode_literals

from .common import *  # noqa: F403
# ruff: noqa: F405

# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env("DJANGO_SECRET_KEY")

# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# DJANGO SECURITY
# https://docs.djangoproject.com/en/dev/topics/security/
# set this to 60 seconds and then to 518400 when you can prove it works
SECURE_HSTS_SECONDS = 60
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
    "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=True
)
SECURE_CONTENT_TYPE_NOSNIFF = env.bool(
    "DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", default=True
)
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SECURE_SSL_REDIRECT = env.bool("DJANGO_SECURE_SSL_REDIRECT", default=True)

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["infinitewarp.com"])
CSRF_TRUSTED_ORIGINS = env.list(
    "DJANGO_CSRF_TRUSTED_ORIGINS", default=["https://*.infinitewarp.com"]
)

# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS += ("gunicorn",)

DATABASES["default"] = env.db("DATABASE_URL")

# https://docs.djangoproject.com/en/dev/topics/cache/#redis
REDIS_URL = env("REDIS_URL", default="redis://127.0.0.1:6379")
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_URL,
    }
}

# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# http://docs.djangoproject.com/en/dev/topics/logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"require_debug_false": {"()": "django.utils.log.RequireDebugFalse"}},
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django.security.DisallowedHost": {
            "level": "ERROR",
            "handlers": ["console"],
            "propagate": True,
        },
    },
}

# Custom Admin URL, use {% url 'admin:index' %}
ADMIN_URL = env("DJANGO_ADMIN_URL")
