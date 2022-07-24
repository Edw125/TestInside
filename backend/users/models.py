from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin, UserManager)
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_superuser(
            self, email, username, first_name, last_name,
            password, **other_fields
    ):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if not other_fields.get("is_staff"):
            raise ValueError("Отказано в доступе")

        if not other_fields.get("is_superuser"):
            raise ValueError("Отказано в доступе")

        return self.create_user(
            email, username, first_name, last_name,
            password=password, **other_fields
        )

    def create_user(self, first_name, last_name,
                    email, password, **other_fields):

        if not email:
            raise ValueError("Укажите email!")

        email = self.normalize_email(email)
        user = self.model(
            email=email, first_name=first_name,
            last_name=last_name, **other_fields
        )

        user.set_password(password)
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        'Имя пользователя', max_length=150, unique=True,
    )
    email = models.EmailField(
        'Электронная почта', max_length=254, unique=True,
    )
    first_name = models.CharField('Имя', max_length=150,)
    last_name = models.CharField('Фамилия', max_length=150,)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.username

    class Meta:
        ordering = ('-username',)

    def __str__(self):
        return self.email


class Logs(models.Model):
    name = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user',
        verbose_name='Пользователь',
    )
    message = models.TextField('Сообщение', blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f'{self.name.username}: {self.message[:15]}'
