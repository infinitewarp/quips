from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from ..quips import models


class CliqueSerializer(ModelSerializer):
    """Clique model serializer."""

    class Meta:
        model = models.Clique
        fields = ["id", "slug"]


class SpeakerSerializer(ModelSerializer):
    """Speaker model serializer."""

    class Meta:
        model = models.Speaker
        fields = ["id", "name"]


class SpeakerSerializerWithCliques(ModelSerializer):
    """Speaker model serializer with clique list."""

    class Meta:
        model = models.Speaker
        fields = ["id", "name", "cliques"]

    cliques = CliqueSerializer(many=True)


class CliqueSerializerWithSpeakers(ModelSerializer):
    """Clique model serializer with speaker list."""

    class Meta:
        model = models.Clique
        fields = ["id", "slug", "speakers"]

    speakers = SerializerMethodField("speaker_list")

    def speaker_list(self, instance):
        serializer = SpeakerSerializer()
        speakers = instance.get_speakers()
        return [serializer.to_representation(speaker) for speaker in speakers]
