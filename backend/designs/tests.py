from django.core.files.uploadedfile import SimpleUploadedFile
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
        self.image = SimpleUploadedFile("design.png", b"not-a-real-image", content_type="image/png")

    def test_health(self):
        response = self.client.get("/api/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_product_options_do_not_require_training_dataset(self):
        response = self.client.get("/api/options/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("long dress", response.json()["categories"])
        self.assertIn("cotton", response.json()["fabrics"])

    def test_offline_core_workflow(self):
        generated = self.client.post("/api/designs/generate/", {**self.payload, "image": self.image}, format="multipart")
        self.assertEqual(generated.status_code, 201, generated.content)
        design_id = generated.json()["id"]
        self.assertEqual(generated.json()["image_source"], "user-upload")

        forecast = self.client.post(f"/api/designs/{design_id}/forecast/", {}, format="json")
        self.assertEqual(forecast.status_code, 503, forecast.content)
        self.assertEqual(forecast.json()["error"]["code"], "FORECAST_MODEL_UNAVAILABLE")

    def test_compare_requires_two_different_designs(self):
        response = self.client.post("/api/designs/compare/", {"design_ids": [1]}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "EXACTLY_TWO_DESIGNS_REQUIRED")

    def test_dashboard_summarizes_saved_designs(self):
        generated = self.client.post("/api/designs/generate/", {**self.payload, "image": self.image}, format="multipart")
        design_id = generated.json()["id"]
        response = self.client.get("/api/dashboard/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["total_designs"], 1)
        self.assertEqual(response.json()["forecasted_designs"], 0)
        self.assertIsNone(response.json()["top_design"])

    def test_design_image_is_required(self):
        response = self.client.post("/api/designs/generate/", self.payload, format="multipart")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"]["code"], "DESIGN_IMAGE_REQUIRED")
