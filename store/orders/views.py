from http import HTTPStatus

import stripe
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

import store.settings
from common.views import TitleMixin
from orders.forms import OrderForm
from orders.models import Order
from products.models import Basket

stripe.api_key = store.settings.STRIPE_SECRET_KEY


class SuccessView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - Спасибо за покупку!'


class CancelledView(TitleMixin, TemplateView):
    template_name = 'orders/canceleld.html'
    title = 'Store - Спасибо за попытку покупки!'


class OrderCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    title = 'Store - Оформление заказа'
    queryset = Basket.objects.all()
    form_class = OrderForm
    success_url = reverse_lazy('orders:create_order')
    
    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)
        line_items = baskets.dict_baskets()

        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            metadata={
                'order_id': self.object.id,
            },
            mode='payment',
            success_url=f'{store.settings.DOMAIN_NAME}{reverse("orders:success_order")}',
            cancel_url=f'{store.settings.DOMAIN_NAME}{reverse("orders:cancel_order")}',
        )

        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)


class AllOrdersView(TitleMixin, ListView):
    queryset = Order.objects.all()
    template_name = 'orders/orders.html'
    title = 'Store - Все заказы'
    ordering = ('-id',)

    def get_queryset(self):
        queryset = super(AllOrdersView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)


class SpecificOrderView(TitleMixin, DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SpecificOrderView, self).get_context_data(object_list=None, **kwargs)
        context['title'] = f'Store - Заказ №{self.object.id}'
        return context


@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    endpoint_secret = store.settings.STRIPE_WEBHOOK_SECRET

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(HTTPStatus.BAD_REQUEST)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(HTTPStatus.BAD_REQUEST)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )

        # Fulfill the purchase...
        fulfill_order(session)

    # Passed signature verification
    return HttpResponse(HTTPStatus.OK)


def fulfill_order(session):
    order_id = int(session.metadata.order_id)
    order = Order.objects.get(id=order_id)
    order.order_paid()
