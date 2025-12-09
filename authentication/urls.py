from django.urls import path

from authentication.views import (
    DeleteUserAPIView,
    LoginAPIView,
    LogoutAPIView,
    RefreshAPIView,
    RegisterAPIView,
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('refresh/', RefreshAPIView.as_view()),
    path('delete/', DeleteUserAPIView.as_view()),
]
