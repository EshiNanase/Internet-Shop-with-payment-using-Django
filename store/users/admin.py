from django.contrib import admin
from users.models import User
from products.admin import BasketAdmin


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'image')
    fields = ('username', 'first_name', 'last_name', 'email', 'image')
    # Указывается в паре с products/admin.py. Позволяет видеть модель внутри другой модели
    inlines = (BasketAdmin,)
