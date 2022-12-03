from django.urls import path
from users.views import login, register

app_name = 'users'

# сюда добавляются конкретные ссылки, например, на товары
urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register')
]
