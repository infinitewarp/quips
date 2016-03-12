# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^$',
        view=views.QuipDefaultView.as_view(),
        name='base'
    ),
    url(
        regex=r'^random/$',
        view=views.QuipCachedRandomView.as_view(),
        name='random'
    ),
    url(
        regex=r'^(?P<uuid>[\d\w\-]+)/$',
        view=views.QuipDetailView.as_view(),
        name='detail'
    ),
]
