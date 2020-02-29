import http

from django.test import TestCase
from django.urls import reverse

from quips.quips import models


class WebsiteViewsTest(TestCase):
    """Website views test case."""

    fixtures = ["trek"]

    def assertQuipInResponse(self, quip, response):
        """Assert the response is OK and the Quip is contained in it."""
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        content = response.content.decode("utf-8")
        self.assertIn(str(quip.uuid), content)

    def test_get_base(self):
        """Test the website's base view."""
        url = reverse("website:base")

        default_quip = models.Quip.objects.all()[0]  # "The First Duty"
        with self.settings(DEFAULT_QUIP_UUID=default_quip.uuid):
            response = self.client.get(url)
        self.assertQuipInResponse(default_quip, response)

    def test_quip_detail(self):
        """Test the website's quip detail view."""
        quip = models.Quip.objects.all()[2]  # "The Best of Both Worlds, Part 1"
        url = reverse("website:detail", args=[str(quip.uuid)])
        response = self.client.get(url)
        self.assertQuipInResponse(quip, response)

    def test_random_quip_speaker_detail(self):
        """Test the website's random quip by speaker view."""
        speaker = models.Speaker.objects.get(id=5)  # Harcourt Fenton Mudd has 1 quip
        quip = models.Quip.objects.filter(quotes__speaker=speaker).get()
        url = reverse("website:random")
        response = self.client.get(url, {"speaker_id": speaker.id})
        self.assertQuipInResponse(quip, response)
