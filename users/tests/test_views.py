from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

import pytest
from rbac.models import Role

User = get_user_model()


@pytest.mark.django_db
def test_update_user_role_success(authorized_client):
    role_manager = Role.objects.create(name='manager')
    user = User.objects.create_user(
        email='user@example.com',
        password='password123',
        role=role_manager,
    )

    role_admin = Role.objects.create(name='admin')
    url = reverse('users:user-role-update-role', args=[user.id])

    payload = {'role_id': role_admin.id}
    response = authorized_client.patch(url, payload, format='json')

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {'status': 'role updated'}

    user.refresh_from_db()
    assert user.role == role_admin


@pytest.mark.django_db
def test_update_user_role_not_found(authorized_client):
    role_admin = Role.objects.create(name='admin')

    url = reverse('users:user-role-update-role', args=[9999])
    payload = {'role_id': role_admin.id}
    response = authorized_client.patch(url, payload, format='json')

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_user_role_invalid_role_id(authorized_client):
    role_manager = Role.objects.create(name='manager')
    user = User.objects.create_user(
        email='user@example.com',
        password='password123',
        role=role_manager,
    )

    url = reverse('users:user-role-update-role', args=[user.id])
    payload = {'role_id': 9999}
    response = authorized_client.patch(url, payload, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'role_id' in response.data


@pytest.mark.django_db
def test_update_user_role_empty_payload(authorized_client):
    role_manager = Role.objects.create(name='manager')
    user = User.objects.create_user(
        email='user@example.com',
        password='password123',
        role=role_manager,
    )

    url = reverse('users:user-role-update-role', args=[user.id])
    response = authorized_client.patch(url, {}, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_update_user_role_unauthorized():
    client = APIClient()

    role_manager = Role.objects.create(name='manager')
    user = User.objects.create_user(
        email='user@example.com',
        password='password123',
        role=role_manager,
    )

    role_admin = Role.objects.create(name='admin')
    url = reverse('users:user-role-update-role', args=[user.id])

    payload = {'role_id': role_admin.id}
    response = client.patch(url, payload, format='json')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_user_role_same_role(authorized_client):
    role_admin = Role.objects.create(name='admin')
    user = User.objects.create_user(
        email='user@example.com',
        password='password123',
        role=role_admin,
    )

    url = reverse('users:user-role-update-role', args=[user.id])
    payload = {'role_id': role_admin.id}
    response = authorized_client.patch(url, payload, format='json')

    assert response.status_code == status.HTTP_200_OK

    user.refresh_from_db()
    assert user.role == role_admin


@pytest.mark.django_db
def test_update_user_role_forbidden(non_admin_client):
    role_manager = Role.objects.create(name='manager')
    user = User.objects.create_user(
        email='user@example.com',
        password='password123',
        role=role_manager,
    )

    role_admin = Role.objects.create(name='admin')
    url = reverse('users:user-role-update-role', args=[user.id])

    payload = {'role_id': role_admin.id}
    response = non_admin_client.patch(url, payload, format='json')

    assert response.status_code == status.HTTP_403_FORBIDDEN
