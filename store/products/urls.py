from django.urls import path
from products.views import products

app_name = 'products'

# сюда добавляются конкретные ссылки, например, на товары
urlpatterns = [
    path('', products, name='index')
]
