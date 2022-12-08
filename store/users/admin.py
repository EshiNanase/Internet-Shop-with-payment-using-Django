from django.contrib import admin

from products.admin import BasketAdmin
from users.models import EmailVerification, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'image')
    fields = ('username', 'first_name', 'last_name', 'email', 'image')
    # Указывается в паре с products/admin.py. Позволяет видеть модель внутри другой модели
    inlines = (BasketAdmin,)


@admin.register(EmailVerification)
class EmailVerification(admin.ModelAdmin):
    list_display = ('code', 'user', 'expiration')
    fields = ('code', 'user', 'expiration', 'created')
    readonly_fields = ('created',)
