from django.test import TestCase
from ego.cars.models.features import Feature


class FeaturesTestCase(TestCase):
    """Testing features endpoints"""

    def setUp(self):
        self.feature = Feature.objects.create(
            title="Transmisión manual",
            description="Lorem ipsum dolor sit",
            image="https://www.example.com/image.jpg",
        )

    def test_features_list_success(self):
        """Verify list of features"""
        response = self.client.get("/features/")
        features = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(features), 1)

    def test_features_detail(self):
        response = self.client.get(f"/features/{str(self.car.uuid)}/")
        feature = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(feature["title"], self.feature.title)
        self.assertEqual(feature["description"], self.feature.description)
        self.assertEqual(feature["image"], self.feature.image)

    def test_features_create_success(self):
        """Verify creation of feature object"""
        payload = {
            "title": "Suspensión mejorada",
            "description": "Lorem ipsum dolor sit",
            "image": "https://www.example.com/image.jpg",
        }
        response = self.client.post("/features/", payload, format="json")
        feature = response.json()
        features = Feature.objects.all()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(feature["title"], payload["title"])
        self.assertEqual(feature["description"], payload["title"])
        self.assertEqual(feature["image"], payload["title"])
        self.assertEqual(len(features), 2)

    def test_features_update_success(self):
        """Update of feature object"""
        payload = {
            "title": "Suspensión mejorada modified",
            "description": "Lorem ipsum dolor sit modified",
            "image": "https://www.example.com/modified.jpg",
        }
        response = self.client.put(f"/features/{str(self.feature.uuid)}")
        self.assertEqual(response.status_code, 200)
        self.feature.refresh_from_db()
        self.assertEqual(self.feature.model, payload["title"])
        self.assertEqual(self.feature.year, payload["description"])
        self.assertEqual(self.feature.price, payload["image"])

    def test_features_patch_success(self):
        """Partial update of feature object"""
        payload = {
            "title": "Suspensión mejorada modified",
        }
        response = self.client.patch(f"/features/{str(self.feature.uuid)}", payload)
        self.assertEqual(response.status_code, 200)
        self.feature.refresh_from_db()
        self.assertEqual(self.feature.model, payload["title"])

    def test_features_delete_success(self):
        """Delete feature object"""
        response = self.client.delete(f"/features/{str(self.feature.uuid)}")
        self.assertEqual(response.status_code, 204)
        features = Feature.objects.all()
        self.assertEqual(len(features), 0)
