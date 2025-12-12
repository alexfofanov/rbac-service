from django.urls import reverse

import pytest

from rbac.models import Role


@pytest.mark.django_db
def test_role_list(authorized_client):
    Role.objects.create(name='Manager')
    url = reverse('rbac:roles-list')
    resp = authorized_client.get(url)

    assert resp.status_code == 200
    assert resp.data[0]['name'] == 'FullAccessRole'
    assert resp.data[1]['name'] == 'Manager'


@pytest.mark.django_db
def test_role_create(authorized_client):
    url = reverse('rbac:roles-list')
    payload = {'name': 'Admin'}
    resp = authorized_client.post(url, payload, format='json')

    assert resp.status_code == 201
    assert Role.objects.filter(name='Admin').exists()


@pytest.mark.django_db
def test_role_detail(authorized_client):
    elem = Role.objects.create(name='DetailRole')
    url = reverse('rbac:roles-detail', args=[elem.id])
    resp = authorized_client.get(url)

    assert resp.status_code == 200
    assert resp.data['id'] == elem.id
    assert resp.data['name'] == elem.name


@pytest.mark.django_db
def test_role_update(authorized_client, full_access_role):
    url = reverse('rbac:roles-detail', args=[full_access_role.id])
    payload = {'name': 'UpdatedRole'}
    resp = authorized_client.put(url, payload, format='json')

    assert resp.status_code == 200
    full_access_role.refresh_from_db()
    assert full_access_role.name == 'UpdatedRole'


@pytest.mark.django_db
def test_role_partial_update(authorized_client, full_access_role):
    url = reverse('rbac:roles-detail', args=[full_access_role.id])
    payload = {'name': 'PartiallyUpdated'}
    resp = authorized_client.patch(url, payload, format='json')

    assert resp.status_code == 200
    full_access_role.refresh_from_db()
    assert full_access_role.name == 'PartiallyUpdated'


@pytest.mark.django_db
def test_role_delete(authorized_client, full_access_role):
    url = reverse('rbac:roles-detail', args=[full_access_role.id])
    resp = authorized_client.delete(url)

    assert resp.status_code == 204
    assert not Role.objects.filter(id=full_access_role.id).exists()
