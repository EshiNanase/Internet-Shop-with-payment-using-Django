from datetime import timedelta

# Для создания юзера стоит использовать AbstractUser т.к. в этом классе уже есть все нужные поля
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now

from store.settings import DOMAIN_NAME, EMAIL_HOST_USER


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    is_verified = models.BooleanField(default=False)


class EmailVerification(models.Model):
    # Эта штука будет генерировать уникальную ссылку для каждого пользователя
    code = models.UUIDField(unique=True)
    # Привязываем юзера
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    # Каждый раз, когда объект будет создаваться, created будет заполняться автоматически
    created = models.DateTimeField(auto_now_add=True)
    # Когда ссылка
    expiration = models.DateTimeField()

    def __str__(self):
        return f'Email Verification for {self.user.email}'

    def send_verification_email(self):
        link = reverse('users:verification', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{DOMAIN_NAME}{link}'
        subject = f'Подтверждение учетной записи для {self.user.username}'
        message = f'Для подтверждения учетной записи для {self.user.username} перейдите по ссылке {verification_link}'
        send_mail(
            subject=subject,
            message=message,
            from_email=EMAIL_HOST_USER,
            recipient_list=(self.user.email,)
        )

    def is_expired(self):
        return True if now() >= self.expiration else False
