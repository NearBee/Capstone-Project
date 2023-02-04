from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    pass

    username = models.CharField(blank=False, unique=True, max_length=25)
    email = models.EmailField(blank=False, unique=True)
    password = models.CharField(blank=False, max_length=128)
    passwordconfirm = models.CharField(blank=False, max_length=128)

    def __str__(self):
        return self.username
