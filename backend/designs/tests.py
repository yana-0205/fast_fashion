from django.test import TestCase
from rest_framework.test import APIClient


class CoreWorkflowTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.payload = {
            "title": "Black linen dress",
            "category": "long dress",
            "color": "black",
            "fabric": "linen",
            "season": "spring-summer",
            "price": "399.00",
            "prompt": "minimal",
            "negative_prompt": "logo",
        }

    def test_health(self):
        response = self.client.get("/api/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_options_are_loaded_from_dataset(self):
        response = self.client.get("/api/options/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("long dress", response.json()["categories"])
        self.assertGreater(len(response.json()["fabrics"]), 10)

    def test_offline_core_workflow(self):
        generated = self.client.post("/api/designs/generate/", self.payload, format="json")
        self.assertEqual(generated.status_code, 201, generated.content)
        design_id = generated.json()["id"]

        forecast = self.client.post(f"/api/designs/{design_id}/forecast/", {}, format="json")
        self.assertEqual(forecast.status_code, 200, forecast.content)
        self.assertEqual(len(forecast.json()["weekly_forecast"]), 10)

        insight = self.client.post(f"/api/designs/{design_id}/insights/", {}, format="json")
        self.assertEqual(insight.status_code, 200, insight.content)
        self.assertEqual(insight.json()["source"], "deterministic-template-v1")

    def test_compare_requires_two_different_designs(self):
        response = self.client.post("/api/designs/compare/", {"design_ids": [1]}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "EXACTLY_TWO_DESIGNS_REQUIRED")
