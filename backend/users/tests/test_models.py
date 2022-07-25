from rest_framework.test import APITestCase

from users.models import User, Logs


class ModelTests(APITestCase):
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

    def test_user_model(self):
        """Проверяем поля модели user."""
        self.assertIsInstance(self.user.username, str)
        self.assertIsInstance(self.user.first_name, str)
        self.assertIsInstance(self.user.last_name, str)
        self.assertIsInstance(self.user.email, str)
        self.assertIsInstance(self.user.is_active, bool)
        self.assertIsInstance(self.user.is_admin, bool)
        self.assertIsInstance(self.user.is_staff, bool)
        self.assertEqual(self.user.get_full_name(), "first_name last_name")
        self.assertEqual(self.user.get_short_name(), "user")
        self.assertEqual(self.user.has_perm(None), False)

    def test_log_model(self):
        """Проверяем поля модели log."""
        self.assertIsInstance(self.log.name, User)
        self.assertIsInstance(self.log.message, str)

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        self.assertEqual(self.log.__str__(), 'user: test')
        self.assertEqual(self.user.__str__(), 'user@example.com')
