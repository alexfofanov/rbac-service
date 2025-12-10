from typing import Iterable

from users.models import User

from rbac.models import PermissionRule


def can(
    user: User, element_name: str, action: str, *, obj_owner_id: int | None = None
) -> bool:
    """Проверка разрешения выполнения действия на элементе"""

    rule = user.get_rule(element_name)
    if not rule:
        return False

    base_attr = f'{action}_permission'
    all_attr = f'{action}_all_permission'

    if obj_owner_id is not None and obj_owner_id == getattr(user, 'id', None):
        return getattr(rule, base_attr, False)

    return getattr(rule, all_attr, False)


def filter_queryset_by_owner(
    qs: Iterable, user: User, rule: PermissionRule | None
) -> list:
    """Фильтрация объектов по owner_id, если у пользователя нет права read_all_permission"""

    if rule and not rule.read_all_permission:
        return [obj for obj in qs if obj.owner_id == user.id]

    return list(qs)
