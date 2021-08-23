from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    first_name = models.TextField(
        'Имя',
        max_length=150,
        blank=False,
        help_text='Required. 150 characters or fewer.'
    )
    last_name = models.TextField(
        'Фамилия',
        max_length=150,
        blank=False,
        help_text='Required. 150 characters or fewer.'
    )
    email = models.EmailField(
        'Адрес электронной почты',
        blank=False,
        unique=True,
        help_text='Required.'
    )


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email