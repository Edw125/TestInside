from http import HTTPStatus

from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import Logs, User


class AuthViewsTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username="user",
            email="user@example.com",
            first_name="first_name",
            last_name="last_name",
            password='admin1234567890',
            is_active=True,
            is_staff=False,
            is_admin=False,
        )
        cls.log = Logs.objects.create(name=cls.user, message="test",)

    def setUp(self):
        self.data = {
            "name": self.log.name.username,
            "message": self.log.message
        }

    @property
    def bearer_token(self):
        refresh = RefreshToken.for_user(self.user)
        return {"HTTP_AUTHORIZATION": f'Bearer {refresh.access_token}'}

    def test_no_auth_post_endpoint(self):
        response = self.client.post('/users/logs/', data=self.data)
        self.assertEqual(self.user.is_active, 1)
        self.assertEqual(response.status_code, HTTPStatus.UNAUTHORIZED)

    def test_auth_post_endpoint(self):
        response = self.client.post('/users/logs/', data=self.data, **self.bearer_token)
        self.assertEqual(self.user.is_active, 1)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
