from django.urls import path

from authentication.views import (
    DeleteUserAPIView,
    LoginAPIView,
    LogoutAPIView,
    RefreshAPIView,
    RegisterAPIView,
)

app_name = 'authentication'

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('refresh/', RefreshAPIView.as_view(), name='refresh'),
    path('delete/', DeleteUserAPIView.as_view(), name='delete'),
]
