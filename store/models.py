from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True, primary_key=True)  # <-- primary key set here
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    # Required permissions methods here...
import os
from django.db import models

def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    if not instance.pk:
        return f'product_images/temp.{ext}'
    return f'product_images/product_{instance.pk}.{ext}'

class Product(models.Model):
    name = models.CharField(max_length=15)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.CharField(max_length=50)
    quantity = models.IntegerField()
    product_status = models.CharField(max_length=150, blank=True, null=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            # Step 1: Temporarily remove image and save to get pk
            image = self.image
            self.image = None
            super().save(*args, **kwargs)

            # Step 2: Restore image and save again, clear flags
            self.image = image
            kwargs.pop("force_insert", None)
            kwargs.pop("force_update", None)

        super().save(*args, **kwargs)

