from PIL import Image
from io import BytesIO

# REST Framework
from rest_framework.test import APITestCase
from rest_framework import status

# Django
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User

# Models
from ego.cars.models.features import Feature


class FeaturesTestCase(APITestCase):
    """Testing features endpoints"""

    def create_test_image(self):
        f = BytesIO()
        image = Image.new("RGB", (100, 100))
        image.save(f, "jpeg")
        f.seek(0)
        return SimpleUploadedFile(
            name="test_image.jpg",
            content=f.read(),
            content_type="image/jpeg",
        )

    def setUp(self):
        self.feature = Feature.objects.create(
            title="Transmisión manual",
            description="Lorem ipsum dolor sit",
            image=self.create_test_image(),
        )
        username = "test_username"
        password = "TestingPassword123"
        User.objects.create_user(email=username, username=username, password=password, is_staff=True, is_superuser=True)
        self.login_payload = {"username": username, "password": password}

    def tearDown(self):
        self.feature.image.delete()
        new_feature = getattr(self, "new_feature", None)
        if new_feature is not None:
            new_feature.image.delete()

    def test_features_list_success(self):
        """Verify list of features"""
        response = self.client.get("/features/")
        features = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(features), 1)

    def test_features_detail(self):
        response = self.client.get(f"/features/{str(self.feature.uuid)}/")
        feature = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(feature["title"], self.feature.title)
        self.assertEqual(feature["description"], self.feature.description)

    def test_features_create_success(self):
        """Verify creation of feature object"""
        response = self.client.post("/internal/login/", self.login_payload)
        self.assertEqual(response.status_code, 200)
        payload = {
            "title": "Suspensión mejorada",
            "description": "Lorem ipsum dolor sit",
            "image": self.create_test_image(),
        }
        response = self.client.post("/features/", payload, format="multipart")
        self.new_feature = Feature.objects.get(uuid=response.json()["uuid"])
        features = Feature.objects.all()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.new_feature.title, payload["title"])
        self.assertEqual(self.new_feature.description, payload["description"])
        self.assertEqual(len(features), 2)

    def test_features_update_success(self):
        """Update of feature object"""
        self.feature.image.delete()
        response = self.client.post("/internal/login/", self.login_payload)
        self.assertEqual(response.status_code, 200)
        payload = {
            "title": "Suspensión mejorada modified",
            "description": "Lorem ipsum dolor sit modified",
            "image": self.create_test_image(),
        }
        response = self.client.put(f"/features/{str(self.feature.uuid)}/", payload, format="multipart")
        self.assertEqual(response.status_code, 200)
        self.feature.refresh_from_db()
        self.assertEqual(self.feature.title, payload["title"])
        self.assertEqual(self.feature.description, payload["description"])

    def test_features_patch_success(self):
        """Partial update of feature object"""
        response = self.client.post("/internal/login/", self.login_payload)
        self.assertEqual(response.status_code, 200)
        payload = {
            "title": "Suspensión mejorada modified",
        }
        response = self.client.patch(f"/features/{str(self.feature.uuid)}/", payload)
        self.assertEqual(response.status_code, 200)
        self.feature.refresh_from_db()
        self.assertEqual(self.feature.title, payload["title"])

    def test_features_delete_success(self):
        """Delete feature object"""
        response = self.client.post("/internal/login/", self.login_payload)
        self.assertEqual(response.status_code, 200)
        response = self.client.delete(f"/features/{str(self.feature.uuid)}/")
        self.assertEqual(response.status_code, 204)
        features = Feature.objects.all()
        self.assertEqual(len(features), 0)


class FeaturesNegativeTestCase(APITestCase):
    """Testing features endpoints (nagative cases)"""

    def create_test_image(self):
        f = BytesIO()
        image = Image.new("RGB", (100, 100))
        image.save(f, "jpeg")
        f.seek(0)
        return SimpleUploadedFile(
            name="test_image.jpg",
            content=f.read(),
            content_type="image/jpeg",
        )

    def setUp(self):
        self.feature = Feature.objects.create(
            title="Transmisión manual",
            description="Lorem ipsum dolor sit",
            image=self.create_test_image(),
        )
        username = "test_username"
        password = "TestingPassword123"
        User.objects.create_user(email=username, username=username, password=password, is_staff=True, is_superuser=True)
        self.login_payload = {"username": username, "password": password}

    def tearDown(self):
        self.feature.image.delete()
        new_feature = getattr(self, "new_feature", None)
        if new_feature is not None:
            new_feature.image.delete()

    def test_features_create_not_authorized(self):
        """Verify creation of feature object is not success if client is not authenticated"""
        payload = {
            "title": "Suspensión mejorada",
            "description": "Lorem ipsum dolor sit",
            "image": self.create_test_image(),
        }
        response = self.client.post("/features/", payload, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_features_update_not_authorized(self):
        """Update of feature object is not success if client is not authenticated"""
        self.feature.image.delete()
        payload = {
            "title": "Suspensión mejorada modified",
            "description": "Lorem ipsum dolor sit modified",
            "image": self.create_test_image(),
        }
        response = self.client.put(f"/features/{str(self.feature.uuid)}/", payload, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_features_patch_not_authorized(self):
        """Partial update of feature object is not success if client is not authenticated"""
        payload = {
            "title": "Suspensión mejorada modified",
        }
        response = self.client.patch(f"/features/{str(self.feature.uuid)}/", payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_features_delete_not_authorized(self):
        """Delete feature object is not success if client is not authenticated"""
        response = self.client.delete(f"/features/{str(self.feature.uuid)}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
