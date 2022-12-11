from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from common.views import TitleMixin

from products.models import Basket
from orders.forms import OrderForm


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    title = 'Store - Оформление заказа'
    queryset = Basket.objects.all()
    form_class = OrderForm
    success_url = reverse_lazy('orders:create_order')

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)


class OrdersView(TitleMixin, TemplateView):
    template_name = 'orders/orders.html'
    title = 'Store - Все заказы'

