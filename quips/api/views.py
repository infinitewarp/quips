from rest_framework import viewsets

from . import serializers
from ..quips import models


class SpeakerViewSet(viewsets.ReadOnlyModelViewSet):
    """List and get speaker instances."""

    queryset = models.Speaker.objects.all()
    serializer_class = serializers.SpeakerSerializerWithCliques


class CliqueViewSet(viewsets.ReadOnlyModelViewSet):
    """List and get clique instances."""

    queryset = models.Clique.objects.all()
    serializer_class = serializers.CliqueSerializerWithSpeakers
