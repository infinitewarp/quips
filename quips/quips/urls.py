# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r'^(?P<pk>[0-9]+)/$',
        view=views.QuipDetailView.as_view(),
        name='detail'
    ),
]
