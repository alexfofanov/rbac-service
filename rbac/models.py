from django.db import models


class Role(models.Model):
    """Роль"""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self) -> str:
        return self.name


class BusinessElement(models.Model):
    """Бизнес-элемент"""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Бизнес-элемент'
        verbose_name_plural = 'Бизнес-элементы'

    def __str__(self) -> str:
        return self.name


class PermissionRule(models.Model):
    """Разрешения роли"""

    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='rules')
    element = models.ForeignKey(
        BusinessElement, on_delete=models.CASCADE, related_name='rules'
    )
    read_permission = models.BooleanField(default=False)
    read_all_permission = models.BooleanField(default=False)
    create_permission = models.BooleanField(default=False)
    update_permission = models.BooleanField(default=False)
    update_all_permission = models.BooleanField(default=False)
    delete_permission = models.BooleanField(default=False)
    delete_all_permission = models.BooleanField(default=False)

    class Meta:
        unique_together = ('role', 'element')
        verbose_name = 'Правило роли доступа'
        verbose_name_plural = 'Правила ролей доступа'

    def __str__(self) -> str:
        return f'{self.role} -> {self.element}'
