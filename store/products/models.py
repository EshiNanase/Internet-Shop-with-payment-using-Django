import stripe
from django.db import models

from store.settings import STRIPE_WEBHOOK_SECRET
from users.models import User

stripe.api_key = STRIPE_WEBHOOK_SECRET


class ProductCategory(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256)
    # null and blank = true => this field can be empty
    description = models.TextField(null=True, blank=True)
    # max_digits - максимальное кол-во цифр, deciaml_places - сколько цифр после запятой
    price = models.IntegerField()
    # value by default is 0, it may be any
    quantity = models.PositiveIntegerField(default=0)
    # upload_to - on download this image should be saved somewhere
    # To work with images you need package Pillow
    image = models.ImageField(upload_to='products_images', null=True, blank=True)
    stripe_price = models.CharField(max_length=128, blank=True, null=True)

    # ForeignKey() - used for linking one model with another. to - what's the linked model.
    # on_delete - CASCADE => если ты удаляешь категорию, а в ней 50 товаров, то все товары тоже удалятся.
    # PROTECT = > категорию нельзя будет удалить, пока не удалены все предметы из этой категории
    # SET_DEFAULT => при удалении категории, в товары ставится значение по умолчанию т.е. в default
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'Продукт: {self.name} | Категория: {self.category.name}'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.stripe_price:
            stripe_product = self.create_stripe_product_price()
            self.stripe_price = stripe_product['id']
        super(Product, self).save(force_insert=False, force_update=False, using=None,
                                  update_fields=None)

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'], unit_amount=round(self.price*100), currency="rub"
        )
        return stripe_product_price


class BasketQuerySet(models.QuerySet):

    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)

    def dict_baskets(self):
        line_items = []
        for basket in self:
            line_items.append({'price': basket.product.stripe_price,
                               'quantity': basket.quantity})
        return line_items


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)

    # Чтобы BasketQuerySet можно было использовать, как менеджер, используем эту команду,
    # т.е. мы можем вызывать методы BasketQuerySet через модель Basket
    objects = BasketQuerySet.as_manager()

    # Поле отвечающее за отображение времени и даты
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт: {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity

    def json_basket(self):
        basket_item = {'product_name': self.product.name,
                       'quantity': self.quantity,
                       'price': float(self.product.price),
                       'sum': float(self.sum())}
        return basket_item
