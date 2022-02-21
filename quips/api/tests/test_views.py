import http

from django.urls import reverse
from rest_framework.test import APITestCase


class ApiViewsTest(APITestCase):
    """API views test case."""

    fixtures = ["trek"]

    def build_random_url(self, query_params=None):
        url = f'http://testserver{reverse("website:random")}'
        if query_params:
            url = (
                url
                + "?"
                + "&".join([f"{key}={value}" for key, value in query_params.items()])
            )
        return url

    def test_get_speaker_detail(self):
        """Test the API's get speaker detail view."""
        speaker_id = 2
        clique_id = 1
        url = reverse("api:speaker-detail", args=[speaker_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        response_json = response.json()
        self.assertEqual(response_json["id"], speaker_id)
        self.assertEqual(response_json["name"], "William Riker")
        self.assertEqual(response_json["cliques"][0]["id"], clique_id)
        self.assertEqual(response_json["cliques"][0]["slug"], "tng")
        self.assertEqual(
            response_json["random_url"],
            self.build_random_url({"speaker_id": speaker_id}),
        )

    def test_get_clique_detail(self):
        """Test the API's get clique detail view."""
        url = reverse("api:clique-detail", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        response_json = response.json()
        self.assertEqual(response_json["id"], 1)
        self.assertEqual(response_json["slug"], "tng")
        self.assertIn({"id": 1, "name": "Jean-Luc Picard"}, response_json["speakers"])

    def test_get_stats_list(self):
        """Test the API's get stats list view."""
        url = reverse("api:stats-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        response_json = response.json()
        self.assertEqual(response_json["clique_count"], 3)
        self.assertEqual(response_json["quip_count"], 6)
        self.assertEqual(response_json["quote_count"], 13)
        self.assertEqual(response_json["speaker_count"], 6)
        self.assertIn(
            {"id": 1, "name": "Jean-Luc Picard", "quip_count": 4, "quote_count": 5},
            response_json["top_speakers"],
        )
