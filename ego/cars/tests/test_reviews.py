# Django
from django.test import TestCase

# Models
from ego.cars.models.cars import Car
from ego.cars.models.reviews import Review
from ego.cars.models.features import Feature

# Utils
from ego.utils.enums.cars_types import CarsTypes


class ReviewsTestCase(TestCase):
    """Testing reviews endpoints"""

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
        )
        self.review = Review.objects.create(
            stars=5, comment="Test comment", car=self.car
        )

    def test_reviews_list_success(self):
        """Verify list of reviews"""
        response = self.client.get("/reviews/")
        self.assertEqual(response.status_code, 200)
        reviews = response.json()
        self.assertEqual(len(reviews), 1)

    def test_review_create_success(self):
        """Verify creation of dealership object"""
        payload = {"comment": "Excellent", "stars": 4, "car": str(self.car.uuid)}
        response = self.client.post("/reviews/", payload)
        self.assertEqual(response.status_code, 201)
        review = response.json()
        reviews = Review.objects.all()
        self.assertEqual(review["comment"], payload["comment"])
        self.assertEqual(review["stars"], payload["stars"])
        self.assertEqual(review["car"], payload["car"])
        self.assertEqual(len(reviews), 2)
