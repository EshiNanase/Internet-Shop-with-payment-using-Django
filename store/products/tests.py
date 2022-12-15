from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from products.models import Product, ProductCategory, Basket
from users.models import User


class IndexViewTestCase(TestCase):

    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductsListViewTestCase(TestCase):
    fixtures = ['product.json', 'product_categories.json']

    def setUp(self):
        self.products = Product.objects.all()

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(list(response.context_data['product_list']), list(self.products[:3]))

    def test_list_with_category(self):
        category = ProductCategory.objects.get(name='Обувь')
        path = reverse('products:category', kwargs={'category_id': category.id})
        response = self.client.get(path)

        self._common_tests(response)
        self.assertEqual(
            list(response.context_data['product_list']),
            list(self.products.filter(category=category.id)[:3])
        )

    def _common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertEqual(response.context_data['title'], 'Store - Каталог')


class BasketOperations(TestCase):
    fixtures = ['product.json', 'product_categories.json']

    def setUp(self):
        self.product = Product.objects.all().last()
        self.path = reverse('products:basket_add', kwargs={'product_id': self.product.id})
        self.user = User.objects.create(username='Green')

    def test_view(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_add(self):
        response = self.client.get(self.path)
        basket = Basket.objects.create(user=self.user, product=self.product, quantity=1)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(basket, Basket.objects.filter(product=self.product).first())

    def test_delete(self):
        response = self.client.get(self.path)
        basket = Basket.objects.create(user=self.user, product=self.product, quantity=1)
        basket_on_delete = Basket.objects.get(id=basket.id)
        basket_on_delete.delete()

        basket = Basket.objects.filter(id=basket_on_delete.id).first()

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(basket)
