import uuid

from django.test import TestCase

from quips.quips import filters, models


class FitersTest(TestCase):
    """Quip queryset filters test case."""

    fixtures = ["trek"]

    def setUp(self):
        self.queryset = models.Quip.objects.all()
        self.clique_sf = models.Clique.objects.get(pk=3)
        self.speaker_picard = models.Speaker.objects.get(pk=1)
        self.speaker_spock = models.Speaker.objects.get(pk=4)
        self.quip_first_duty = models.Quip.objects.get(pk=1)
        self.quip_unification = models.Quip.objects.get(pk=4)
        self.quip_i_mudd = models.Quip.objects.get(pk=5)

    def test_filter_by_uuid(self):
        known_quip = self.quip_first_duty
        uuid_string = str(known_quip.uuid)
        filtered_quip = filters.filter_by_uuid(self.queryset, uuid_string).get()
        self.assertEqual(known_quip, filtered_quip)

    def test_filter_by_uuid_not_found(self):
        uuid_string = str(uuid.uuid4())
        queryset = filters.filter_by_uuid(self.queryset, uuid_string)
        self.assertEqual(queryset.count(), 0)

    def test_filter_by_uuid_bad_uuid(self):
        uuid_string = "1234-nota-real-uuid"
        with self.assertRaises(filters.InputNotValidUUID):
            filters.filter_by_uuid(self.queryset, uuid_string)

    def test_filter_by_speaker_name(self):
        known_speaker = self.speaker_picard
        speaker_quip = self.quip_first_duty
        not_speaker_quip = self.quip_i_mudd
        filtered_quips = filters.filter_by_speaker_name(
            self.queryset, known_speaker.name
        ).all()
        self.assertIn(speaker_quip, filtered_quips)
        self.assertNotIn(not_speaker_quip, filtered_quips)

    def test_filter_by_speaker_name_not_found(self):
        unknown_name = "Ed Mercer"
        queryset = filters.filter_by_speaker_name(self.queryset, unknown_name)
        self.assertEqual(queryset.count(), 0)

    def test_filter_by_speaker_id(self):
        known_speaker = self.speaker_picard
        speaker_quip = self.quip_first_duty
        not_speaker_quip = self.quip_i_mudd
        filtered_quips = filters.filter_by_speaker_id(
            self.queryset, known_speaker.id
        ).all()
        self.assertIn(speaker_quip, filtered_quips)
        self.assertNotIn(not_speaker_quip, filtered_quips)

    def test_filter_by_clique(self):
        sf_clique_slug = self.clique_sf.slug
        sf_quips = filters.filter_by_clique(self.queryset, sf_clique_slug).all()
        self.assertIn(self.quip_first_duty, sf_quips)
        self.assertIn(self.quip_unification, sf_quips)
        self.assertNotIn(self.quip_i_mudd, sf_quips)

    def test_filter_by_clique_not_found(self):
        sf_clique_slug = self.clique_sf.slug
        sf_quips = filters.filter_by_clique(self.queryset, sf_clique_slug).all()
        self.assertIn(self.quip_first_duty, sf_quips)
        self.assertIn(self.quip_unification, sf_quips)
        self.assertNotIn(self.quip_i_mudd, sf_quips)

    def test_filter_by_speaker_id_and_filter_by_clique(self):
        quips_by_speaker_id = filters.filter_by_speaker_id(
            self.queryset, self.speaker_spock.id
        )
        quips_by_speaker_and_clique = filters.filter_by_clique(
            quips_by_speaker_id, self.clique_sf.slug
        )
        sf_spock_quips = quips_by_speaker_and_clique.all()

        self.assertNotIn(self.quip_first_duty, sf_spock_quips)
        self.assertIn(self.quip_unification, sf_spock_quips)
        self.assertNotIn(self.quip_i_mudd, sf_spock_quips)
