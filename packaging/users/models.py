from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Пользователь"""

    OPTION_ONE = 'admin'
    OPTION_TWO = 'manager'
    OPTION_THREE = 'worker'

    OPTIONS = [
        (OPTION_ONE, 'Администратор'),
        (OPTION_TWO, 'Менеджер'),
        (OPTION_THREE, 'Работник'),

    ]
    position = models.CharField(
        'Статус',
        max_length=10,
        choices=OPTIONS,
        default=OPTION_ONE
    )
    first_name = models.CharField(
        'Имя',
        max_length=50
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=50
    )
    avatar = models.ImageField(
        'Аватар',
        upload_to='user/',
        blank=True, null=True
    )
    phone_number = models.CharField(
        'Телефон',
        max_length=15,
        blank=True,
        null=True
    )
    address = models.TextField(
        'Адрес',
        blank=True,
        null=True
    )

    email = models.EmailField(unique=True)
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)

    class Meta:
        verbose_name = 'сотрудника'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return f'{self.first_name}'


class Client(models.Model):
    """Пользователь"""

    company_name = models.CharField(
        'Компания',
        max_length=100,
        blank=True,
        null=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=50
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=50,
        blank=True,
        null=True
    )
    phone_number = models.CharField(
        'Телефон',
        max_length=15,
        null=False,
        blank=False,
    )
    address = models.TextField(
        'Адрес',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'клиента'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.company_name if self.company_name else f"Client {self.pk}"

    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    updated_at = models.DateTimeField("Дата обновления", auto_now=True)
