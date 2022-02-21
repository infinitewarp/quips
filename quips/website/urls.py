# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.urls import path

from . import views

urlpatterns = [
    path("", view=views.QuipDefaultView.as_view(), name="base"),
    path("random/", view=views.QuipRandomSpeakerView.as_view(), name="random"),
    path(
        "clique/<slug>/",
        view=views.QuipRandomCliqueSpeakerView.as_view(),
        name="cliquerandom",
    ),
    path("<uuid>/", view=views.QuipDetailView.as_view(), name="detail"),
]
