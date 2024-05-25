from django.contrib.auth.models import AbstractUser
from django.db import models


class Member(AbstractUser):
    first_name = None
    last_name = None

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]
