from django.urls import path

from authentication.views import (
    DeleteUserAPIView,
    LoginAPIView,
    LogoutAPIView,
    RefreshAPIView,
    RegisterAPIView,
)

urlpatterns = [
    path('auth/register', RegisterAPIView.as_view()),
    path('auth/login', LoginAPIView.as_view()),
    path('auth/logout', LogoutAPIView.as_view()),
    path('auth/refresh', RefreshAPIView.as_view()),
    path('auth/delete', DeleteUserAPIView.as_view()),
]
