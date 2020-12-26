import http
import json
import uuid

from django.test import TestCase
from django.urls import reverse

from quips.quips import models


class SlackappViewsTest(TestCase):
    """Slack app views test case."""

    fixtures = ["trek"]

    def setUp(self):
        self.quip_first_duty = models.Quip.objects.get(id=1)
        self.quip_i_mudd = models.Quip.objects.get(id=5)
        self.quip_city = models.Quip.objects.get(id=6)
        self.speaker_riker = models.Speaker.objects.get(id=2)
        self.clique_tos = models.Clique.objects.get(id=2)

    def assertValidResponse(self, content, status_code, ephemeral=False):
        self.assertEqual(status_code, http.HTTPStatus.OK)
        if ephemeral:
            self.assertEqual(content["response_type"], "ephemeral")
        else:
            self.assertNotEqual(content.get("response_type", ""), "ephemeral")
            self.assertIn("blocks", content)
            self.assertTrue(len(content["blocks"]) > 0)
        return content

    def extract_response(self, response):
        content_string = response.content.decode("utf-8")
        content_dict = json.loads(content_string)
        return content_dict, response.status_code

    def extract_uuid_string_from_content(self, content):
        # This split should be reliable because the URL is always in the last block.
        uuid_string = (
            content["blocks"][-1]["elements"][0]["text"]
            .split("|")[0]
            .split("<")[1]
            .split("/")[-2]
        )
        return uuid_string

    def test_post_empty(self):
        """Assert handling a POST with no payload."""
        url = reverse("slackapp:slackbot")
        response = self.client.post(url)
        content, status_code = self.extract_response(response)
        self.assertValidResponse(content, status_code)

    def test_post_uuid(self):
        """Assert handling a POST containing a Quip UUID."""
        quip = self.quip_first_duty
        uuid_string = str(quip.uuid)
        post_body = {"text": uuid_string}
        url = reverse("slackapp:slackbot")
        expected_url = reverse("website:detail", args=(uuid_string,))

        response = self.client.post(url, post_body)
        content, status_code = self.extract_response(response)

        self.assertValidResponse(content, status_code)
        self.assertIn(
            quip.quotes.first().text,
            content["blocks"][0]["text"]["text"],
        )
        self.assertIn(
            expected_url,
            content["blocks"][-1]["elements"][0]["text"],
        )

    def test_post_uuid_not_found(self):
        """Assert handling a POST containing a UUID not matching any Quip."""
        bogus_uuid_string = str(uuid.uuid4())
        post_body = {"text": bogus_uuid_string}
        url = reverse("slackapp:slackbot")

        response = self.client.post(url, post_body)
        content, status_code = self.extract_response(response)

        self.assertValidResponse(content, status_code, ephemeral=True)
        self.assertIn("No quip found", content["text"])
        self.assertIn(bogus_uuid_string, content["text"])

    def test_post_speaker_name_part(self):
        """Assert handling a POST containing part of a Speaker name."""
        speaker_name = self.speaker_riker.name
        name_part = speaker_name.split(" ")[-1]
        post_body = {"text": name_part}
        url = reverse("slackapp:slackbot")

        response = self.client.post(url, post_body)
        content, status_code = self.extract_response(response)

        self.assertValidResponse(content, status_code)
        uuid_string = self.extract_uuid_string_from_content(content)
        quip = models.Quip.objects.get(uuid=uuid_string)
        quip_speakers = [quote.speaker for quote in quip.quotes.all()]
        self.assertIn(self.speaker_riker, quip_speakers)

    def test_post_clique(self):
        """Assert handling a POST containing a valid Clique slug."""
        clique_slug = self.clique_tos.slug
        post_body = {"text": clique_slug}
        url = reverse("slackapp:slackbot")

        response = self.client.post(url, post_body)
        content, status_code = self.extract_response(response)

        self.assertValidResponse(content, status_code)
        uuid_string = self.extract_uuid_string_from_content(content)
        # The UUID should match only one of these two known Quips.
        self.assertIn(
            uuid_string, (str(self.quip_i_mudd.uuid), str(self.quip_city.uuid))
        )

    def test_post_no_quip_found(self):
        """Assert handling a POST containing a value that can find no Quip."""
        speaker_name = "Washburne"
        post_body = {"text": speaker_name}
        url = reverse("slackapp:slackbot")

        response = self.client.post(url, post_body)
        content, status_code = self.extract_response(response)

        self.assertValidResponse(content, status_code, ephemeral=True)
        self.assertIn("No quip found", content["text"])
        self.assertIn(speaker_name, content["text"])
