from django.test import TestCase
from django.urls import reverse, reverse_lazy
from orders.models import Order
from users.models import User
from http import HTTPStatus


class SuccessViewTestCase(TestCase):

    def test_view(self):
        path = reverse('orders:success_order')
        response = self.client.get(path)

        self.assertEqual(response, 'orders/success.html')
        self.assertEqual(response.context_data['title'], 'Store - Спасибо за покупку!')


class CancelledViewTestCase(TestCase):

    def test_view(self):
        path = reverse('orders:cancel_order')
        response = self.client.get(path)

        self.assertEqual(response, 'orders/canceleld.html')
        self.assertEqual(response.context_data['title'], 'Store - Спасибо за попытку покупки!')


class OrderCreateViewTestCase(TestCase):
    fixtures = ['order.json', 'user.json']

    def test_view(self):
        path = reverse_lazy('orders:create_order')
        response = self.client.get(path)

        self.assertEqual(response.context_data['title'], 'Store - Оформление заказа')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'orders/order-create.html')


class OrderListViewTestCase(TestCase):
    fixtures = ['order.json', 'user.json']

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.client.force_login(user=self.user)
        self.orders = Order.objects.filter(initiator=self.user).order_by('-id')

    def test_list(self):
        path = reverse('orders:all_orders')
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(list(response.context_data['order_list']), list(self.orders))

    def _common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'orders/orders.html')
        self.assertEqual(response.context_data['title'], 'Store - Все заказы')


class SpecificOrderTestCase(TestCase):
    fixtures = ['order.json', 'user.json']

    def setUp(self):
        self.order = Order.objects.all().last()

    def test_view(self):
        path = reverse('orders:specific_order', kwargs={'pk': self.order.id})
        response = self.client.get(path)
        self._common_tests(response)
        self.assertEqual(
            response.context_data['order'],
            self.order
        )

    def _common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'orders/order.html')
        self.assertEqual(response.context_data['title'], f'Store - Заказ №{self.order.id}')

