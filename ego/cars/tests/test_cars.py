from PIL import Image
from io import BytesIO

# Django
from django.core.files.uploadedfile import SimpleUploadedFile

# REST Framework
from rest_framework.test import APITestCase

# Utils
from ego.utils.enums.cars_types import CarsTypes

# Models
from ego.cars.models.cars import Car
from ego.cars.models.features import Feature
from ego.cars.models.reviews import Review


class CarsTestCase(APITestCase):
    """Testing cars endpoints"""

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
        self.car = Car.objects.create(
            car_type=CarsTypes.AUTOS,
            model="Auto Test",
            year=2024,
            price=1000000,
            title="Preparada para cualquier desafío",
            description="Lorem ipsum dolor sit",
            image=self.create_test_image(),
        )
        self.review = Review.objects.create(
            stars=5, comment="Test comment", car=self.car
        )

    def tearDown(self):
        self.car.image.delete()
        self.feature.image.delete()
        new_car = getattr(self, "new_car", None)
        if new_car is not None:
            new_car.image.delete()

    def test_cars_list_success(self):
        """Verify list of cars"""
        response = self.client.get("/cars/")
        cars = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(cars), 1)

    def test_ascending_order_by_price(self):
        """Ordering car list by price (ascending)"""
        self.new_car = Car.objects.create(
            car_type=CarsTypes.AUTOS,
            model="Auto Test 2",
            year=2024,
            price=2000000,
            title="Preparada para cualquier desafío",
            description="Lorem ipsum dolor sit",
            image=self.create_test_image(),
        )
        response = self.client.get("/cars/?ordering=price")
        cars = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(cars[0]["price"] < cars[1]["price"])

    def test_descending_order_by_price(self):
        """Ordering car list by price (descending)"""
        self.new_car = Car.objects.create(
            car_type=CarsTypes.AUTOS,
            model="Auto Test 2",
            year=2024,
            price=2000000,
            title="Preparada para cualquier desafío",
            description="Lorem ipsum dolor sit",
            image=self.create_test_image(),
        )
        response = self.client.get("/cars/?ordering=-price")
        cars = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(cars[0]["price"] > cars[1]["price"])

    def test_ascending_order_by_year(self):
        """Ordering car list by year (ascending)"""
        self.new_car = Car.objects.create(
            car_type=CarsTypes.AUTOS,
            model="Auto Test 2",
            year=2020,
            price=1000000,
            title="Preparada para cualquier desafío",
            description="Lorem ipsum dolor sit",
            image=self.create_test_image(),
        )
        response = self.client.get("/cars/?order=year")
        cars = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(cars[0]["year"] < cars[1]["year"])

    def test_descending_order_by_year(self):
        """Ordering car list by year (descending)"""
        self.new_car = Car.objects.create(
            car_type=CarsTypes.AUTOS,
            model="Auto Test 2",
            year=2020,
            price=1000000,
            title="Preparada para cualquier desafío",
            description="Lorem ipsum dolor sit",
            image=self.create_test_image(),
        )
        response = self.client.get("/cars/?ordering=-year")
        cars = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(cars[0]["year"] > cars[1]["year"])

    def test_cars_detail(self):
        response = self.client.get(f"/cars/{str(self.car.uuid)}/")
        car = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(car["model"], self.car.model)
        self.assertEqual(car["year"], self.car.year)
        self.assertEqual(car["car_type"], self.car.car_type)

    def test_cars_create_success(self):
        """Verify creation of car object"""
        payload = {
            "car_type": CarsTypes.AUTOS,
            "model": "Auto Test New",
            "year": 2024,
            "price": 1000000,
            "title": "Preparada para cualquier desafío",
            "description": "Lorem ipsum dolor sit",
            "image": self.create_test_image(),
        }
        response = self.client.post("/cars/", payload, format="multipart")
        self.new_car = Car.objects.get(uuid=response.json()["uuid"])
        cars = Car.objects.all()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.new_car.model, payload["model"])
        self.assertEqual(self.new_car.year, payload["year"])
        self.assertEqual(self.new_car.car_type, payload["car_type"])
        self.assertEqual(len(cars), 2)

    def test_cars_update_success(self):
        """Update of car object"""
        self.car.image.delete()
        payload = {
            "car_type": CarsTypes.AUTOS,
            "model": "Auto Modified",
            "year": 2023,
            "price": 2000000,
            "title": "Preparada para cualquier desafío",
            "description": "Lorem ipsum dolor sit",
            "image": self.create_test_image(),
        }
        response = self.client.put(
            f"/cars/{str(self.car.uuid)}/", payload, format="multipart"
        )
        self.assertEqual(response.status_code, 200)
        self.car.refresh_from_db()
        self.assertEqual(self.car.model, payload["model"])
        self.assertEqual(self.car.year, payload["year"])
        self.assertEqual(self.car.price, payload["price"])

    def test_cars_patch_success(self):
        """Partial update of car object"""
        payload = {
            "model": "Auto Modified",
        }
        response = self.client.patch(f"/cars/{str(self.car.uuid)}/", payload)
        self.assertEqual(response.status_code, 200)
        self.car.refresh_from_db()
        self.assertEqual(self.car.model, payload["model"])

    def test_cars_add_feature_success(self):
        """Add car features"""
        payload = {
            "car_id": str(self.car.uuid),
            "feature_id": str(self.feature.uuid),
        }
        response = self.client.post(f"/cars/add_feature/", payload)
        self.assertEqual(response.status_code, 200)
        self.car.refresh_from_db()
        car_features = [str(feature.uuid) for feature in self.car.features.all()]
        self.assertIn(str(self.feature.uuid), car_features)

    def test_cars_delete_success(self):
        """Delete car object"""
        response = self.client.delete(f"/cars/{str(self.car.uuid)}/")
        self.assertEqual(response.status_code, 204)
        cars = Car.objects.all()
        self.assertEqual(len(cars), 0)

    def test_car_reviews_list_success(self):
        """Verify list of car reviews"""
        payload = {"car_id": str(self.car.uuid)}
        response = self.client.post(f"/cars/reviews/", payload)
        reviews = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(reviews["reviews"]), 1)
        self.assertEqual(reviews["avg_rating"], self.review.stars)
        self.assertEqual(reviews["reviews"][0]["comment"], self.review.comment)
