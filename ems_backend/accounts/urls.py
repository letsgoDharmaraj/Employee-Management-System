from django.urls import path
from .views import RegisterUserView
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from .views import RequestPasswordResetView, PasswordResetConfirmView


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('password-reset/', RequestPasswordResetView.as_view(), name='password-reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
