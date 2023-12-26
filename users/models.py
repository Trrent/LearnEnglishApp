import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager


class User(AbstractUser):
    id = models.CharField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(max_length=255, unique=True)
    username = None
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.email}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
