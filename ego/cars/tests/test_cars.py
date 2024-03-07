from django.test import TestCase
from ego.cars.models.cars import Car
from ego.cars.models.features import Feature
from ego.utils.enums.cars_types import CarsTypes


class CarsTestCase(TestCase):
    """Testing cars endpoints"""

    def setUp(self):
        self.feature = Feature.objects.create(
            title="Transmisión manual",
            description="Lorem ipsum dolor sit",
            image="https://www.example.com/image.jpg",
        )
        self.car = Car.objects.create(
            car_type=CarsTypes.AUTOS,
            model="Auto Test",
            year=2024,
            price=1000000,
            title="Preparada para cualquier desafío",
            description="Lorem ipsum dolor sit",
            image="https://www.example.com/image.jpg",
            features=[self.feature],
        )

    def test_cars_list_success(self):
        """Verify list of cars"""
        response = self.client.get("/cars/")
        cars = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(cars), 1)

    def test_ascending_order_by_price(self):
        """Ordering car list by price (ascending)"""
        response = self.client.get("/cars/?order=price")
        cars = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(cars[0].price < cars[1].price)

    def test_descending_order_by_price(self):
        """Ordering car list by price (descending)"""
        response = self.client.get("/cars/?order=-price")
        cars = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(cars[0].price > cars[1].price)

    def test_ascending_order_by_year(self):
        """Ordering car list by year (ascending)"""
        response = self.client.get("/cars/?order=year")
        cars = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(cars[0].year < cars[1].year)

    def test_descending_order_by_year(self):
        """Ordering car list by year (descending)"""
        response = self.client.get("/cars/?order=-year")
        cars = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(cars[0].year > cars[1].year)

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
            "model": "Auto Test",
            "year": 2024,
            "price": 1000000,
            "title": "Preparada para cualquier desafío",
            "description": "Lorem ipsum dolor sit",
            "image": "https://www.example.com/image.jpg",
            "features": [self.feature],
        }
        response = self.client.post("/cars/", payload, format="json")
        car = response.json()
        cars = Car.objects.all()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(car["model"], payload["model"])
        self.assertEqual(car["year"], payload["year"])
        self.assertEqual(car["car_type"], payload["car_type"])
        self.assertIn(self.feature, car["features"])
        self.assertEqual(len(cars), 2)

    def test_cars_update_success(self):
        """Update of car object"""
        payload = {
            "car_type": CarsTypes.AUTOS,
            "model": "Auto Modified",
            "year": 2023,
            "price": 2000000,
            "title": "Preparada para cualquier desafío",
            "description": "Lorem ipsum dolor sit",
            "image": "https://www.example.com/image.jpg",
            "features": [self.feature],
        }
        response = self.client.put(f"/cars/{str(self.car.uuid)}")
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
        response = self.client.patch(f"/cars/{str(self.car.uuid)}", payload)
        self.assertEqual(response.status_code, 200)
        self.car.refresh_from_db()
        self.assertEqual(self.car.model, payload["model"])

    def test_cars_delete_success(self):
        """Delete car object"""
        response = self.client.delete(f"/cars/{str(self.car.uuid)}")
        self.assertEqual(response.status_code, 204)
        cars = Car.objects.all()
        self.assertEqual(len(cars), 0)
