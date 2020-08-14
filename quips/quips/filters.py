import uuid

from quips.quips.models import Clique, Speaker


def filter_by_uuid(queryset, uuid_string):
    """Filter a Quip-based queryset by UUID."""
    try:
        quip_uuid = uuid.UUID(uuid_string)
    except ValueError:
        raise InputNotValidUUID()
    queryset = queryset.filter(uuid=quip_uuid)
    if queryset.count() == 0:
        raise QuipUuidNotFound()
    return queryset


def filter_by_speaker_name(queryset, speaker_name):
    """Filter a Quip-based queryset by Quote's Speaker's name."""
    try:
        speaker = Speaker.objects.filter(name__icontains=speaker_name).first()
        if speaker is None:
            raise SpeakerNameNotFound()
        queryset = queryset.filter(quotes__speaker=speaker)
    except queryset.model.DoesNotExist:
        raise SpeakerNameNotFound()
    return queryset


def filter_by_speaker_id(queryset, speaker_id):
    """Filter a Quip-based queryset by Quote's Speaker's id."""
    if speaker_id is None:
        return queryset
    speaker = Speaker.objects.filter(pk=speaker_id).first()
    queryset = queryset.filter(quotes__speaker=speaker)
    return queryset


def filter_by_clique_and_speaker_id(queryset, clique_slug, speaker_id):
    """Filter a Quip-based queryset by Clique and optionally Speaker's id."""
    clique = Clique.objects.filter(slug=clique_slug)
    speakers = Speaker.objects.filter(cliques__in=clique)
    if speaker_id is not None:
        speakers = speakers.filter(pk=speaker_id)
    queryset = queryset.filter(quotes__speaker__in=speakers)
    return queryset


class SpeakerNameNotFound(Exception):
    """A Quip with the given Speaker name was not found."""


class QuipUuidNotFound(Exception):
    """A Quip with the given UUID was not found."""


class InputNotValidUUID(Exception):
    """The provided input string was not a valid UUID."""
