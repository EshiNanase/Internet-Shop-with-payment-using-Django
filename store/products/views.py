from django.shortcuts import render, HttpResponse


def index(request):
    context = {
        'title': 'Home'
    }
    return render(request, 'products/index.html', context)


def store(request):
    context = {
        'title': 'Store',
        'products': [
            {
                'image': '/static/vendor/img/products/Adidas-hoodie.png',
                'product': 'Худи черного цвета с монограммами adidas Originals',
                'price': '6 090,00',
                'material': 'Мягкая ткань для свитшотов. Стиль и комфорт – это образ жизни.'
            },
            {
                'image': '/static/vendor/img/products/Blue-jacket-The-North-Face.png',
                'product': 'Синяя куртка The North Face',
                'price': '23 725,00',
                'material': 'Гладкая ткань. Водонепроницаемое покрытие. Легкий и теплый пуховый наполнитель.'
            },
            {
                'image': '/static/vendor/img/products/Brown-sports-oversized-top-ASOS-DESIGN.png',
                'product': 'Коричневый спортивный oversized-топ ASOS DESIGN',
                'price': '3 390,00',
                'material': 'ММатериал с плюшевой текстурой. Удобный и мягкий.'
            },
        ]

    }
    return render(request, 'products/products.html', context)
