from django.db import models
from users.models import User


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
    image = models.ImageField(upload_to='products_images')

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


class BasketQuerySet(models.QuerySet):

    def total_sum(self):
        return sum(basket.sum() for basket in self)

    def total_quantity(self):
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)

    # Чтобы BasketQuerySet можно было использовать, как менеджер, используем эту команду, т.е. мы можем вызывать методы BasketQuerySet через модель Basket
    objects = BasketQuerySet.as_manager()

    # Поле отвечающее за отображение времени и даты
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт: {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity
