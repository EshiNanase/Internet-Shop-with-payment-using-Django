from django.contrib.auth.decorators import login_required
from django.urls import path

from users.views import (EmailVerificationView, UserLoginView, UserLogoutView,
                         UserProfileView, UserRegistrationCreateView)

app_name = 'users'

# сюда добавляются конкретные ссылки, например, на товары
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegistrationCreateView.as_view(), name='register'),
    path('profile/<int:pk>', login_required(UserProfileView.as_view()), name='profile'),
    path('logout/', login_required(UserLogoutView.as_view()), name='logout'),
    path('verification/<str:email>/<uuid:code>', EmailVerificationView.as_view(), name='verification')
]
