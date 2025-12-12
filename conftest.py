import pytest
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

from authentication.jwt import create_access_token, create_refresh_token

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user():
    def make_user(**kwargs):
        password = kwargs.pop('password', 'password123')
        user = User.objects.create_user(**kwargs)
        user.set_password(password)
        user.save()
        return user

    return make_user


@pytest.fixture
def auth_user(api_client, create_user):
    user = create_user(email='auth@example.com', password='password123')
    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
    return user, access, refresh, api_client
