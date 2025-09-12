from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        CLIENT = 'client', 'Client'
        PREPARATEUR = 'preparateur', 'Préparateur'
        CAISSIER = 'caissier', 'Caissier'
        ADMIN = 'admin', 'Admin'

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    role = models.CharField(max_length=16, choices=Role.choices, default=Role.CLIENT)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.username} ({self.role})"
