from http import HTTPStatus

from rest_framework.test import APIClient, APITestCase

from users.models import User, Logs


class URLTests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username="user",
            email="user@example.com",
            first_name="first_name",
            last_name="last_name",
            is_active=True,
            is_staff=False,
            is_admin=False,
        )
        cls.log = Logs.objects.create(name=cls.user, message="test",)

    def setUp(self):
        self.authorized_client = APIClient()
        self.authorized_client.force_authenticate(user=self.user)
        self.data = {
            "name": self.log.name.username,
            "message": self.log.message
        }
        self.command_history = {
            "name": self.log.name.username,
            "message": "history 10"
        }

    def test_status_url_logs(self):
        """Проверка доступа к url users/logs/."""
        response = self.authorized_client.get('/users/logs/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.authorized_client.post('/users/logs/', data=self.data)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        response = self.authorized_client.delete(f'/users/logs/{self.log.id}/')
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

    def test_content_url_logs(self):
        """Проверка  данных ответа эндпоинта users/logs/."""
        response = self.authorized_client.post('/users/logs/', data=self.data)
        self.assertEqual(response.data, {'detail': 'Запись успешно добавлена'})
        response = self.authorized_client.post(
            '/users/logs/', data=self.command_history
        )
        self.assertEqual(response.data.count(), 2)
        response = self.authorized_client.delete(f'/users/logs/{self.log.id}/')
        self.assertEqual(response.data, {'detail': 'Запись удалена'})
        response = self.authorized_client.delete(f'/users/logs/{self.log.id}/')
        self.assertEqual(response.data, {'detail': 'Записи не существует'})
