from django.urls import path
from products.views import products, basket_add, basket_delete

app_name = 'products'

# сюда добавляются конкретные ссылки, например, на товары
urlpatterns = [
    path('', products, name='index'),
    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),
    path('baskets/delete/<int:basket_id>/', basket_delete, name='basket_delete')
]

