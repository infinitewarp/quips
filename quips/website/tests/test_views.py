import http

from django.test import TestCase
from django.urls import reverse

from quips.quips import models


class WebsiteViewsTest(TestCase):
    """Website views test case."""

    fixtures = ["trek"]

    def assertResponseOK(self, response):
        """Assert the response is OK, and return the decoded content."""
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        content = response.content.decode("utf-8")
        return content

    def assertResponseNotFound(self, response):
        """Assert the response is Not Found, and return the decoded content."""
        self.assertEqual(response.status_code, http.HTTPStatus.NOT_FOUND)
        content = response.content.decode("utf-8")
        return content

    def assertQuipInResponse(self, quip, response):
        """Assert the response is OK and the Quip is contained in it."""
        content = self.assertResponseOK(response)
        quip_url = reverse("website:detail", args=[str(quip.uuid)])
        self.assertIn(quip_url, content)
        if quip.context:
            # Just check for the first word of context.
            self.assertIn(quip.context.split()[0], content)
        return content

    def test_get_base(self):
        """Test the website's base view."""
        url = reverse("website:base")

        default_quip = models.Quip.objects.get(id=1)  # "The First Duty"
        with self.settings(DEFAULT_QUIP_UUID=str(default_quip.uuid)):
            response = self.client.get(url)
        self.assertQuipInResponse(default_quip, response)

    def test_quip_detail(self):
        """Test the website's quip detail view."""
        quip = models.Quip.objects.get(id=3)  # "The Best of Both Worlds, Part 1"
        url = reverse("website:detail", args=[str(quip.uuid)])
        response = self.client.get(url)
        self.assertQuipInResponse(quip, response)

    def test_quip_detail_malformed_uuid(self):
        """Test the website's quip detail view when given a malformed UUID."""
        malformed_uuid_string = "1234-nota-real-uuid"
        url = reverse("website:detail", args=[malformed_uuid_string])
        response = self.client.get(url)
        self.assertResponseNotFound(response)

    def test_random_quip_speaker_detail(self):
        """Test the website's random quip by speaker view."""
        speaker = models.Speaker.objects.get(id=5)  # Harcourt Fenton Mudd has 1 quip
        quip = models.Quip.objects.filter(quotes__speaker=speaker).get()
        url = reverse("website:random")
        response = self.client.get(url, {"speaker_id": speaker.id})
        self.assertQuipInResponse(quip, response)

    def test_cliquerandom_detail(self):
        """Test the website's random quip by clique detail view."""
        clique = models.Clique.objects.get(id=1)  # TNG
        clique_url = reverse("website:cliquerandom", args=[clique.slug])
        response = self.client.get(clique_url)
        content = self.assertResponseOK(response)
        self.assertIn(clique_url, content)

    def test_cliquerandom_with_speaker_detail(self):
        """Test the website's random quip by clique detail view."""
        clique = models.Clique.objects.get(id=1)  # TNG
        speaker = models.Speaker.objects.get(id=4)  # Spock has 1 TNG quip
        quip = models.Quip.objects.get(id=4)  # "Unification, Part 2"
        clique_url = reverse("website:cliquerandom", args=[clique.slug])
        response = self.client.get(clique_url, {"speaker_id": speaker.id})
        content = self.assertQuipInResponse(quip, response)
        self.assertIn(clique_url, content)
