from django.contrib.auth import get_user_model

import pytest
from authentication.jwt import create_access_token

from rbac.models import BusinessElement, PermissionRule, Role

User = get_user_model()


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
