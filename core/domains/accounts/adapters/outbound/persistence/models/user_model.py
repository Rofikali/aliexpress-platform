form django.db import models
from django_cryptography.fields import encrypt


class UserModel(models.Model):
    email = encrypt(models.EmailField())
    phone = encrypt(models.CharField(max_length=20))
