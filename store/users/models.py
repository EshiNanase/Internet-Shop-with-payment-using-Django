from django.db import models

# Для создания юзера стоит использовать AbstractUser т.к. в этом классе уже есть все нужные поля
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
