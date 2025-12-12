from django.urls import reverse

import pytest

from rbac.models import PermissionRule, Role


@pytest.mark.django_db
def test_permission_rule_list(authorized_client, full_access_role, rbac_element):
    another_role = Role.objects.create(name='AnotherRole')
    PermissionRule.objects.create(
        role=another_role, element=rbac_element, read_permission=True
    )

    url = reverse('rbac:permission-rule-list')
    resp = authorized_client.get(url)

    assert resp.status_code == 200
    assert len(resp.data) == 2


@pytest.mark.django_db
def test_permission_rule_create(authorized_client, rbac_element):
    role = Role.objects.create(name='CreatorRole')

    url = reverse('rbac:permission-rule-list')
    payload = {
        'role': role.id,
        'element_id': rbac_element.id,
        'role_id': role.id,
        'read_permission': True,
        'create_permission': True,
    }
    resp = authorized_client.post(url, payload, format='json')
    print(resp.data)

    assert resp.status_code == 201
    assert PermissionRule.objects.filter(role=role, element=rbac_element).exists()


@pytest.mark.django_db
def test_permission_rule_unique_constraint(
    authorized_client, full_access_role, rbac_element
):
    url = reverse('rbac:permission-rule-list')
    payload = {
        'role': full_access_role.id,
        'element': rbac_element.id,
        'read_permission': True,
    }

    resp = authorized_client.post(url, payload, format='json')

    assert resp.status_code == 400


@pytest.mark.django_db
def test_permission_rule_detail(authorized_client, full_access_role, rbac_element):
    rule = PermissionRule.objects.get(role=full_access_role, element=rbac_element)

    url = reverse('rbac:permission-rule-detail', args=[rule.id])
    resp = authorized_client.get(url)

    assert resp.status_code == 200
    assert resp.data['id'] == rule.id
    assert resp.data['role']['id'] == full_access_role.id
    assert resp.data['element']['id'] == rbac_element.id


@pytest.mark.django_db
def test_permission_rule_partial_update(
    authorized_client, full_access_role, rbac_element
):
    rule = PermissionRule.objects.get(role=full_access_role, element=rbac_element)

    url = reverse('rbac:permission-rule-detail', args=[rule.id])
    payload = {'create_permission': False}

    resp = authorized_client.patch(url, payload, format='json')

    assert resp.status_code == 200
    rule.refresh_from_db()
    assert rule.create_permission is False


@pytest.mark.django_db
def test_permission_rule_delete(authorized_client, full_access_role, rbac_element):
    rule = PermissionRule.objects.get(role=full_access_role, element=rbac_element)

    url = reverse('rbac:permission-rule-detail', args=[rule.id])
    resp = authorized_client.delete(url)

    assert resp.status_code == 204
    assert not PermissionRule.objects.filter(id=rule.id).exists()
