import time
from functools import lru_cache

from django.db.models import Count

from .models import Clique, Quip, Quote, Speaker


def get_cached_stats(expiry: int = 5 * 60, *args, **kwargs) -> dict:
    """Get various cached stats about quips models."""
    when = time.time() // expiry
    return cached_stats(when, *args, **kwargs)


@lru_cache()
def cached_stats(when: int, *args, **kwargs) -> dict:
    """
    Build various stats about quips models.

    Note: ``when`` argument is only used to key the LRU cache.
    """
    return _build_stats(*args, **kwargs)


def _build_stats(top_count: int = 5) -> dict:
    """Build various stats about quips models."""
    top_speakers = Speaker.objects.annotate(
        count=Count("quote__quip", distinct=True)
    ).order_by("-count", "id")
    stats = {
        "clique_count": Clique.objects.count(),
        "quip_count": Quip.objects.count(),
        "quote_count": Quote.objects.count(),
        "speaker_count": Speaker.objects.count(),
        "top_speakers": [
            {"id": speaker.id, "name": speaker.name, "count": speaker.count}
            for speaker in top_speakers[:top_count]
        ],
    }
    return stats
