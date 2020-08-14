import uuid

from quips.quips.models import Clique, Quote, Speaker


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
    """
    Filter a Quip-based queryset by Clique and optionally Speaker's id.

    The input queryset should be a Quip-based queryset.

    The queryset construction is rather complicated because the output should
    be quips wherein all of their quotes belong to speakers in the same clique.
    Quotes that have quotes where only some speakers are in the clique should
    be excluded from output. This means having to build and exclude multiple
    subqueries to get only what we want.

    Each step of the queryset construction is documented inline for clarify.
    """
    all_quips = queryset

    # Find all speakers in the clique.
    clique = Clique.objects.filter(slug=clique_slug)
    clique_speakers = Speaker.objects.filter(cliques__in=clique)

    # Find all of the *other* speakers *not* in the clique.
    not_clique_speakers = Speaker.objects.difference(clique_speakers)

    # Find all quotes having speakers *not* in the clique.
    # NOTE: Forcing match on the id *should not* be necessary here.
    # There seems to be a bug in Django because having the simpler
    # `speaker__in=not_clique_speakers` results in a generated query
    # using a sub-select returning all Speaker columns but the outer
    # query matching only on the id, and that raises an error about
    # mismatched number of columns. Forcing both outer and inner to
    # use only the id seems to work around this problem.
    not_clique_quotes = Quote.objects.filter(
        speaker_id__in=not_clique_speakers.values("id")
    )

    # Find all quips containing those quotes from not-clique speakers.
    # quips = queryset.exclude(quote_id__in=not_clique_quotes.values("id"))
    exclude_quips = queryset.filter(quotes__in=not_clique_quotes)

    # Optionally filter the base set of all quips on the requested speaker.
    if speaker_id:
        all_quips = all_quips.filter(quotes__speaker_id=speaker_id)

    # Find all *other* quips *not* having the excluded quotes.
    # This should result on quotes with *all* their speakers in the clique.
    all_quips = all_quips.difference(exclude_quips)

    return all_quips


class SpeakerNameNotFound(Exception):
    """A Quip with the given Speaker name was not found."""


class QuipUuidNotFound(Exception):
    """A Quip with the given UUID was not found."""


class InputNotValidUUID(Exception):
    """The provided input string was not a valid UUID."""
