# store/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomeUSer(AbstractUser):
    contact = models.CharField(max_length=15)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.username
