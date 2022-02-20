# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", view=views.QuipDefaultView.as_view(), name="base"),
    path("random/", view=views.QuipRandomSpeakerView.as_view(), name="random"),
    re_path(
        r"^clique/(?P<slug>.+)/$",
        view=views.QuipRandomCliqueSpeakerView.as_view(),
        name="cliquerandom",
    ),
    re_path(
        r"^(?P<uuid>[\d\w\-]+)/$",
        view=views.QuipDetailView.as_view(),
        name="detail",
    ),
]
