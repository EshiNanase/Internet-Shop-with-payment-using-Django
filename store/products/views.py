from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from products.models import Product, ProductCategory, Basket
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def index(request):
    context = {
        'title': 'Home'
    }
    return render(request, 'products/index.html', context)


def products(request, category_id=None, page_number=1):
    if category_id:
        products = Product.objects.filter(category=category_id)
    else:
        products = Product.objects.all()

    per_page = 3
    paginator = Paginator(products, per_page)
    products_paginator = paginator.page(page_number)

    context = {'title': 'Store - Каталог',
               'categories': ProductCategory.objects.all(),
               'products': products_paginator}
    return render(request, 'products/products.html', context)


@login_required
def basket(request):
    context = {
        'title': 'Корзина'
    }
    return render(request, 'orders/order.html', context)


@login_required
def basket_add(request, product_id):
    # Продукт, который кладем в корзину
    product = Product.objects.get(id=product_id)

    # Делаем проверку, есть ли такие же продукты в корзине (но это лист)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    # Возвращаем пользователя на ту же страницу, где он был
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_delete(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])

