from django.contrib import admin

from products.models import Basket, Product, ProductCategory

# admin.site.register(Product)
admin.site.register(ProductCategory)


# Указываем с какой моделью будем работать в админке. Чтобы не ругался, нужно удалить строчку без декоратора, см. выше
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    # Указываем, что будет показываться в админке в таблице
    list_display = ('name', 'price', 'quantity', 'category')
    # Создаем переменную филдс и перечисляем в ней все поля, чтобы было красиво в админке
    # Чтобы в админке показывать несколько переменных на одной строке, нужно создать кортеж в кортеже
    fields = ('name', 'description', ('price', 'quantity'), 'image', 'stripe_price', 'category')
    # Переменная показывающая какие поля нельзя менять в админке
    readonly_fields = ('description',)
    # Поля для поиска в админке
    search_fields = ('name',)
    # Переменная для определенного порядка (алфавитного, по цене) в админке
    ordering = ('name',)


# Наследование admin.TabularInline позволяет добавить эту модель вовнутрь другой модели, если указать model.
# В этом примере я подключаю корзину к пользователю т.е. я буду видеть корзину пользователя, если укажу в users/admin.py
class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity',)
    # extra по умолчанию стоит три, это доп. поля, который будем видеть в админке. Лучше поменять на 0, шоб было красиво
    extra = 0
