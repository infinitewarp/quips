from rest_framework import viewsets
from rest_framework.response import Response

from . import serializers
from ..quips import models
from ..quips.stats import get_cached_stats


class SpeakerViewSet(viewsets.ReadOnlyModelViewSet):
    """List and get speaker instances."""

    queryset = models.Speaker.objects.all()
    serializer_class = serializers.SpeakerSerializerWithCliques


class CliqueViewSet(viewsets.ReadOnlyModelViewSet):
    """List and get clique instances."""

    queryset = models.Clique.objects.all()
    serializer_class = serializers.CliqueSerializerWithSpeakers


class StatsViewSet(viewsets.ViewSet):
    """List quips stats."""

    def list(self, *args, **kwargs):
        """Get current server stats."""
        response = get_cached_stats()
        return Response(response)
