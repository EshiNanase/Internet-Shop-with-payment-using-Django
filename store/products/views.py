from django.shortcuts import render, HttpResponse


def index(request):
    return render(request, 'products/index.html')


def store(request):
    return render(request, 'products/products.html')
