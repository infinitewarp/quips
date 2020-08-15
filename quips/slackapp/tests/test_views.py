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
        self.quip_first_duty = models.Quip.objects.get(pk=1)
        self.speaker_riker = models.Speaker.objects.get(pk=2)

    def assertValidResponse(self, response, in_channel=True, contents=None):
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        content = response.content.decode("utf-8")
        content_dict = json.loads(content)
        if in_channel:
            self.assertEqual(content_dict["response_type"], "in_channel")
        else:
            self.assertEqual(content_dict["response_type"], "ephemeral")
        if contents:
            for content in contents:
                self.assertIn(content, content_dict["text"])
        return content_dict

    def test_post_empty(self):
        """Assert handling a POST with no payload."""
        url = reverse("slackapp:slackbot")
        response = self.client.post(url)
        self.assertValidResponse(
            response, contents=[": "]  # the typical speaker:quote delimiter.
        )

    def test_post_uuid(self):
        """Assert handling a POST containing a Quip UUID."""
        uuid_string = str(self.quip_first_duty.uuid)
        post_body = {"text": uuid_string}
        url = reverse("slackapp:slackbot")
        expected_url = reverse("website:detail", args=(uuid_string,))
        response = self.client.post(url, post_body)
        self.assertValidResponse(
            response,
            contents=[
                self.quip_first_duty.quotes.first().text,
                uuid_string,
                expected_url,
            ],
        )

    def test_post_uuid_not_found(self):
        """Assert handling a POST containing a UUID not matching any Quip."""
        bogus_uuid_string = str(uuid.uuid4())
        post_body = {"text": bogus_uuid_string}
        url = reverse("slackapp:slackbot")
        response = self.client.post(url, post_body)
        self.assertValidResponse(
            response, in_channel=False, contents=["No quip found", bogus_uuid_string],
        )

    def test_post_speaker_name_part(self):
        """Assert handling a POST containing part of a Speaker name."""
        speaker_name = self.speaker_riker.name
        name_part = speaker_name.split(" ")[-1]
        post_body = {"text": name_part}
        url = reverse("slackapp:slackbot")
        response = self.client.post(url, post_body)
        content_dict = self.assertValidResponse(response)

        # This split should be reliable because the URL is always on the last line.
        response_url_uuid = content_dict["text"].split()[-1].split("/")[-2]
        quip = models.Quip.objects.get(uuid=response_url_uuid)
        quip_speakers = [quote.speaker for quote in quip.quotes.all()]
        self.assertIn(self.speaker_riker, quip_speakers)

    def test_post_speaker_name_not_found(self):
        """Assert handling a POST containing an unrecognized Speaker name."""
        speaker_name = "Washburne"
        post_body = {"text": speaker_name}
        url = reverse("slackapp:slackbot")
        response = self.client.post(url, post_body)
        self.assertValidResponse(
            response, in_channel=False, contents=["No quip found", speaker_name]
        )
