import faker
from django.test import TestCase

from .. import models, stats

FAKER = faker.Faker()


class StatsTest(TestCase):
    """Stats calculation test case."""

    fixtures = ["trek"]

    def test_build_stats(self) -> None:
        """Test stats are built appropriately with known fixture data."""
        the_stats = stats._build_stats()
        self.assertEqual(the_stats["clique_count"], 3)
        self.assertEqual(the_stats["quip_count"], 6)
        self.assertEqual(the_stats["quote_count"], 13)
        self.assertEqual(the_stats["speaker_count"], 6)
        self.assertEqual(len(the_stats["top_speakers"]), 5)

        # Picard is the true top quipper.
        self.assertEqual(the_stats["top_speakers"][0]["id"], 1)
        self.assertEqual(the_stats["top_speakers"][0]["name"], "Jean-Luc Picard")
        self.assertEqual(the_stats["top_speakers"][0]["quip_count"], 4)
        self.assertEqual(the_stats["top_speakers"][0]["quote_count"], 5)

        # Riker, Spock, and Kirk all have equal quip counts.
        # Kirk has a greater quote count, putting him at a higher rank.
        # Spock and Riker must use id ascending to break the tie.
        self.assertEqual(the_stats["top_speakers"][1]["id"], 6)
        self.assertEqual(the_stats["top_speakers"][1]["name"], "James T. Kirk")
        self.assertEqual(the_stats["top_speakers"][1]["quip_count"], 2)
        self.assertEqual(the_stats["top_speakers"][1]["quote_count"], 3)
        self.assertEqual(the_stats["top_speakers"][2]["id"], 2)
        self.assertEqual(the_stats["top_speakers"][2]["name"], "William Riker")
        self.assertEqual(the_stats["top_speakers"][2]["quip_count"], 2)
        self.assertEqual(the_stats["top_speakers"][2]["quote_count"], 2)
        self.assertEqual(the_stats["top_speakers"][3]["id"], 4)
        self.assertEqual(the_stats["top_speakers"][3]["name"], "Spock")
        self.assertEqual(the_stats["top_speakers"][3]["quip_count"], 2)
        self.assertEqual(the_stats["top_speakers"][3]["quote_count"], 2)

        self.assertEqual(the_stats["top_speakers"][4]["id"], 5)
        self.assertEqual(the_stats["top_speakers"][4]["name"], "Harcourt Fenton Mudd")
        self.assertEqual(the_stats["top_speakers"][4]["quip_count"], 1)
        self.assertEqual(the_stats["top_speakers"][4]["quote_count"], 1)

    def test_cached_stats(self) -> None:
        """Test stats are cached until the "when" argument changes."""
        self.assertEqual(models.Speaker.objects.count(), 6)
        original_stats = stats.cached_stats(1)
        models.Speaker.objects.create(name=FAKER.name())
        self.assertEqual(models.Speaker.objects.count(), 7)
        outdated_stats = stats.cached_stats(1)
        self.assertEqual(original_stats, outdated_stats)
        refreshed_stats = stats.cached_stats(2)
        self.assertNotEqual(original_stats, refreshed_stats)
        self.assertEqual(refreshed_stats["speaker_count"], 7)
