import uuid

from django.test import TestCase

from quips.quips import filters, models


class FitersTest(TestCase):
    """Quip queryset filters test case."""

    fixtures = ["trek"]

    def setUp(self):
        self.queryset = models.Quip.objects.all()
        self.speaker_picard = models.Speaker.objects.get(pk=1)
        self.quip_first_duty = models.Quip.objects.get(pk=1)
        self.quip_i_mudd = models.Quip.objects.get(pk=5)

    def test_filter_by_uuid(self):
        known_quip = self.quip_first_duty
        uuid_string = str(known_quip.uuid)
        filtered_quip = filters.filter_by_uuid(self.queryset, uuid_string).get()
        self.assertEqual(known_quip, filtered_quip)

    def test_filter_by_uuid_not_found(self):
        uuid_string = str(uuid.uuid4())
        with self.assertRaises(filters.QuipUuidNotFound):
            filters.filter_by_uuid(self.queryset, uuid_string)

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
        with self.assertRaises(filters.SpeakerNameNotFound):
            filters.filter_by_speaker_name(self.queryset, unknown_name)

    def test_filter_by_speaker_id(self):
        known_speaker = self.speaker_picard
        speaker_quip = self.quip_first_duty
        not_speaker_quip = self.quip_i_mudd
        filtered_quips = filters.filter_by_speaker_id(
            self.queryset, known_speaker.id
        ).all()
        self.assertIn(speaker_quip, filtered_quips)
        self.assertNotIn(not_speaker_quip, filtered_quips)
