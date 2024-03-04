from django.db import models
from .manager import CustomUserManager
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    GENDER = (("male", "Male"), ("female", "Female"))

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True, db_index=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER, null=True, blank=True)
    is_verified = models.BooleanField(default=False, null=True, blank=True)
    is_active = models.BooleanField(default=False, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self) -> str:
        return f"{self.last_name} {self.first_name}"
