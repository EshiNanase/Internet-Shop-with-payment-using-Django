from django.urls import path
from django.views.decorators.cache import cache_page

from orders.views import OrdersView, OrderCreateView

app_name = 'orders'


# сюда добавляются конкретные ссылки, например, на товары
urlpatterns = [
    path('<int:user_id>/', OrdersView.as_view(), name='orders'),
    path('create/', OrderCreateView.as_view(), name='create_order'),
]
