from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import EmailVerification, User


class UserRegistrationViewTestCase(TestCase):

    def setUp(self):
        self.path = reverse('users:register')
        self.data = {
            'first_name': 'Sasha',
            'last_name': 'Turkish',
            'email': 'alksndr.zln@gmail.com',
            'username': 'Green',
            'password1': 'TestPasswordYolo1',
            'password2': 'TestPasswordYolo1'
        }
        self.username = self.data['username']

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Регистрация')
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_registration_post_success(self):
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username))

        response = self.client.post(self.path, self.data)

        # check user creation
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username))

        # check email verification
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification)
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )

    def test_user_registration_post_error(self):
        User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)

        self.assertTrue(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)


class UserLoginViewTestCase(TestCase):
    path = reverse('users:login')

    def test_view(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Авторизация')
        self.assertTemplateUsed(response, 'users/login.html')
