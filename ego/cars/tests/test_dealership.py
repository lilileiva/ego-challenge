from django.test import TestCase
from ego.cars.models.dealership import Dealership
from ego.utils.enums.provinces import Provinces


class DealershipTestCase(TestCase):
    """Testing delaerships endpoints"""

    def setUp(self):
        self.dealership = Dealership.objects.create(
            address="Test 1234", province=Provinces.BUENOS_AIRES, phone=12123123
        )

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
        payload = {"address": "New 1234", "province": Provinces.SALTA, "phone": 2222222}
        response = self.client.post(
            "/dealership/", data=payload, content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        feature = response.json()
        dealerships = Dealership.objects.all()
        self.assertEqual(feature["address"], payload["address"])
        self.assertEqual(feature["province"], payload["province"])
        self.assertEqual(feature["phone"], payload["phone"])
        self.assertEqual(len(dealerships), 2)

    def test_dealerships_update_success(self):
        """Update of feature object"""
        payload = {
            "address": "Modified 1234",
            "province": Provinces.CHACO,
            "phone": 1111111,
        }
        response = self.client.put(
            f"/dealership/{str(self.dealership.uuid)}/",
            payload,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.dealership.refresh_from_db()
        self.assertEqual(self.dealership.address, payload["address"])
        self.assertEqual(self.dealership.province, payload["province"])
        self.assertEqual(self.dealership.phone, payload["phone"])

    def test_dealerships_patch_success(self):
        """Partial update of feature object"""
        payload = {
            "province": Provinces.CHACO,
        }
        response = self.client.patch(
            f"/dealership/{str(self.dealership.uuid)}/",
            payload,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.dealership.refresh_from_db()
        self.assertEqual(self.dealership.province, payload["province"])

    def test_dealerships_delete_success(self):
        """Delete feature object"""
        response = self.client.delete(f"/dealership/{str(self.dealership.uuid)}/")
        self.assertEqual(response.status_code, 204)
        dealerships = Dealership.objects.all()
        self.assertEqual(len(dealerships), 0)
