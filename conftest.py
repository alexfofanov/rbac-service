from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

import pytest
from authentication.jwt import create_access_token, create_refresh_token
from rbac.models import BusinessElement, PermissionRule, Role

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


@pytest.fixture
def rbac_element():
    return BusinessElement.objects.create(name='rbac')


@pytest.fixture
def full_access_role(rbac_element):
    role = Role.objects.create(name='FullAccessRole')
    PermissionRule.objects.create(
        role=role,
        element=rbac_element,
        read_permission=True,
        read_all_permission=True,
        create_permission=True,
        update_permission=True,
        update_all_permission=True,
        delete_permission=True,
        delete_all_permission=True,
    )
    return role


@pytest.fixture
def user(full_access_role):
    return User.objects.create_user(
        email='admin@example.com',
        first_name='Admin',
        last_name='User',
        password='password123',
        role=full_access_role,
    )


@pytest.fixture
def authorized_client(api_client, user):
    access = create_access_token(user.id)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
    return api_client


@pytest.fixture
def read_only_access_role(rbac_element):
    role = Role.objects.create(name='ReadOnlyAccessRole')
    PermissionRule.objects.create(
        role=role,
        element=rbac_element,
        read_permission=True,
        read_all_permission=True,
        create_permission=False,
        update_permission=False,
        update_all_permission=False,
        delete_permission=False,
        delete_all_permission=False,
    )


@pytest.fixture
def read_only_user(read_only_access_role):
    return User.objects.create_user(
        email='read_only_user@example.com',
        first_name='Admin',
        last_name='User',
        password='password123',
        role=read_only_access_role,
    )


@pytest.fixture
def non_admin_client(api_client, read_only_user):
    access = create_access_token(read_only_user.id)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
    return api_client
