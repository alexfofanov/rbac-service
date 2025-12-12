from django.urls import reverse

import pytest

from rbac.models import BusinessElement


@pytest.mark.django_db
def test_business_element_list(authorized_client):
    BusinessElement.objects.create(name='elem1')
    BusinessElement.objects.create(name='elem2')

    url = reverse('rbac:elements-list')
    resp = authorized_client.get(url)

    assert resp.status_code == 200
    assert len(resp.data) == 3
    assert resp.data[1]['name'] == 'elem1'
    assert resp.data[2]['name'] == 'elem2'


@pytest.mark.django_db
def test_business_element_create(authorized_client):
    url = reverse('rbac:elements-list')
    payload = {'name': 'NewElement'}
    resp = authorized_client.post(url, payload, format='json')

    assert resp.status_code == 201
    assert BusinessElement.objects.filter(name='NewElement').exists()


@pytest.mark.django_db
def test_business_element_detail(authorized_client):
    elem = BusinessElement.objects.create(name='DetailElement')
    url = reverse('rbac:elements-detail', args=[elem.id])
    resp = authorized_client.get(url)

    assert resp.status_code == 200
    assert resp.data['id'] == elem.id
    assert resp.data['name'] == elem.name


@pytest.mark.django_db
def test_business_element_update(authorized_client):
    elem = BusinessElement.objects.create(name='OldName')

    url = reverse('rbac:elements-detail', args=[elem.id])
    payload = {'name': 'UpdatedName'}
    resp = authorized_client.put(url, payload, format='json')

    assert resp.status_code == 200
    elem.refresh_from_db()
    assert elem.name == 'UpdatedName'


@pytest.mark.django_db
def test_business_element_partial_update(authorized_client):
    elem = BusinessElement.objects.create(name='Initial')

    url = reverse('rbac:elements-detail', args=[elem.id])
    payload = {'name': 'Partial'}
    resp = authorized_client.patch(url, payload, format='json')

    assert resp.status_code == 200
    elem.refresh_from_db()
    assert elem.name == 'Partial'


@pytest.mark.django_db
def test_business_element_delete(authorized_client):
    elem = BusinessElement.objects.create(name='ToDelete')

    url = reverse('rbac:elements-detail', args=[elem.id])
    resp = authorized_client.delete(url)

    assert resp.status_code == 204
    assert not BusinessElement.objects.filter(id=elem.id).exists()
