from django.contrib.auth import get_user_model
from django.urls import reverse

import pytest

User = get_user_model()


@pytest.mark.django_db
def test_register_user(api_client):
    url = reverse('authentication:register')
    data = {
        'email': 'test@example.com',
        'first_name': 'Test',
        'last_name': 'User',
        'password': 'password123',
    }
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert 'id' in response.json()
    assert User.objects.filter(email='test@example.com').exists()


@pytest.mark.django_db
def test_login_user(api_client, create_user):
    user = create_user(email='login@example.com', password='password123')
    url = reverse('authentication:login')
    data = {'email': 'login@example.com', 'password': 'password123'}
    response = api_client.post(url, data)
    json_data = response.json()
    assert response.status_code == 200
    assert 'access' in json_data
    assert 'refresh' in json_data


@pytest.mark.django_db
def test_login_user_invalid_credentials(api_client, create_user):
    create_user(
        email='login@example.com',
        first_name='Test',
        last_name='User',
        password='password123',
    )
    url = reverse('authentication:login')
    data = {'email': 'login@example.com', 'password': 'wrongpassword'}
    response = api_client.post(url, data)
    assert response.status_code == 400
    assert 'Invalid credentials' in response.json()['non_field_errors']


@pytest.mark.django_db
def test_refresh_token(auth_user):
    user, access, refresh, client = auth_user
    url = reverse('authentication:refresh')
    data = {'refresh': refresh}
    response = client.post(url, data)
    json_data = response.json()
    assert response.status_code == 200
    assert 'access' in json_data


@pytest.mark.django_db
def test_delete_user(auth_user):
    user, access, refresh, client = auth_user
    url = reverse('authentication:delete')
    response = client.delete(url)
    assert response.status_code == 200
    assert response.json()['detail'] == 'Soft deleted'
    user.refresh_from_db()
    assert user.is_deleted
