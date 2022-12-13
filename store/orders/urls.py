from django.urls import path

from orders.views import (AllOrdersView, CancelledView, OrderCreateView,
                          SpecificOrderView, SuccessView)

app_name = 'orders'


# сюда добавляются конкретные ссылки, например, на товары
urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='create_order'),
    path('success/', SuccessView.as_view(), name='success_order'),
    path('cancel/', CancelledView.as_view(), name='cancel_order'),
    path('all/', AllOrdersView.as_view(), name='all_orders'),
    path('specific/<int:pk>/', SpecificOrderView.as_view(), name='specific_order'),
]
