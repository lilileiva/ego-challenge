from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from rest_framework.test import APITestCase


class AccountsTestCase(APITestCase):

    def setUp(self):
        self.username = "test_user"
        self.password = "TestingPass123"
        User.objects.create_user(
            email=self.username,
            username=self.username,
            password=self.password,
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

    def test_login(self):
        payload = {"username": self.username, "password": self.password}
        url = "/internal/login/"
        response = self.client.post(url, payload)
        sessions = Session.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(sessions), 1)

    def test_register(self):
        payload = {"username": "new_user", "password": self.password, "repeat_password": self.password}
        url = "/internal/register/"
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, 201)
        users = User.objects.all()
        self.assertEqual(len(users), 2)
