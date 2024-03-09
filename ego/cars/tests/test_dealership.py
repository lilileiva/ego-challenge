# Django
from django.contrib.auth.models import User

# Django REST Framework
from rest_framework.test import APITestCase
from rest_framework import status

# Project
from ego.cars.models.dealership import Dealership
from ego.utils.enums.provinces import Provinces


class DealershipTestCase(APITestCase):
    """Testing delaerships endpoints"""

    def setUp(self):
        self.dealership = Dealership.objects.create(
            address="Test 1234", province=Provinces.BUENOS_AIRES, phone=12123123
        )
        username = "test_username"
        password = "TestingPassword123"
        User.objects.create_user(email=username, username=username, password=password, is_staff=True, is_superuser=True)
        self.login_payload = {"username": username, "password": password}

    def test_dealerships_list_success(self):
        """Verify list of dealerships"""
        response = self.client.get("/dealership/")
        self.assertEqual(response.status_code, 200)
        dealerships = response.json()
        self.assertEqual(len(dealerships), 1)

    def test_dealerships_detail(self):
        response = self.client.get(f"/dealership/{str(self.dealership.uuid)}/")
        dealership = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(dealership["address"], self.dealership.address)
        self.assertEqual(dealership["province"], self.dealership.province)
        self.assertEqual(dealership["phone"], self.dealership.phone)

    def test_dealerships_create_success(self):
        """Verify creation of dealership object"""
        response = self.client.post("/internal/login/", self.login_payload)
        self.assertEqual(response.status_code, 200)
        payload = {"address": "New 1234", "province": Provinces.SALTA, "phone": 2222222}
        response = self.client.post("/dealership/", data=payload)
        self.assertEqual(response.status_code, 201)
        feature = response.json()
        dealerships = Dealership.objects.all()
        self.assertEqual(feature["address"], payload["address"])
        self.assertEqual(feature["province"], payload["province"])
        self.assertEqual(feature["phone"], payload["phone"])
        self.assertEqual(len(dealerships), 2)

    def test_dealerships_update_success(self):
        """Update of dealership object"""
        response = self.client.post("/internal/login/", self.login_payload)
        self.assertEqual(response.status_code, 200)
        payload = {
            "address": "Modified 1234",
            "province": Provinces.CHACO,
            "phone": 1111111,
        }
        response = self.client.put(
            f"/dealership/{str(self.dealership.uuid)}/",
            payload,
        )
        self.assertEqual(response.status_code, 200)
        self.dealership.refresh_from_db()
        self.assertEqual(self.dealership.address, payload["address"])
        self.assertEqual(self.dealership.province, payload["province"])
        self.assertEqual(self.dealership.phone, payload["phone"])

    def test_dealerships_patch_success(self):
        """Partial update of dealership object"""
        response = self.client.post("/internal/login/", self.login_payload)
        self.assertEqual(response.status_code, 200)
        payload = {
            "province": Provinces.CHACO,
        }
        response = self.client.patch(f"/dealership/{str(self.dealership.uuid)}/", payload)
        self.assertEqual(response.status_code, 200)
        self.dealership.refresh_from_db()
        self.assertEqual(self.dealership.province, payload["province"])

    def test_dealerships_delete_success(self):
        """Delete dealership object"""
        response = self.client.post("/internal/login/", self.login_payload)
        self.assertEqual(response.status_code, 200)
        response = self.client.delete(f"/dealership/{str(self.dealership.uuid)}/")
        self.assertEqual(response.status_code, 204)
        dealerships = Dealership.objects.all()
        self.assertEqual(len(dealerships), 0)


class DealershipNegativeTestCase(APITestCase):
    """Testing delaerships endpoints"""

    def setUp(self):
        self.dealership = Dealership.objects.create(
            address="Test 1234", province=Provinces.BUENOS_AIRES, phone=12123123
        )
        username = "test_username"
        password = "TestingPassword123"
        User.objects.create_user(email=username, username=username, password=password, is_staff=True, is_superuser=True)
        self.login_payload = {"username": username, "password": password}

    def test_dealerships_create_not_authenticated(self):
        """Verify creation of dealership object is not success if client is not authenticated"""
        payload = {"address": "New 1234", "province": Provinces.SALTA, "phone": 2222222}
        response = self.client.post("/dealership/", data=payload, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_dealerships_update_not_authenticated(self):
        """Update of dealership object is not success if client is not authenticated"""
        payload = {
            "address": "Modified 1234",
            "province": Provinces.CHACO,
            "phone": 1111111,
        }
        response = self.client.put(
            f"/dealership/{str(self.dealership.uuid)}/",
            payload,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_dealerships_patch_not_authorized(self):
        """Partial update of dealership object is not success if client is not authenticated"""
        payload = {
            "province": Provinces.CHACO,
        }
        response = self.client.patch(
            f"/dealership/{str(self.dealership.uuid)}/",
            payload,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_dealerships_delete_not_authorized(self):
        """Delete dealership object is not success if client is not authenticated"""
        response = self.client.delete(f"/dealership/{str(self.dealership.uuid)}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
