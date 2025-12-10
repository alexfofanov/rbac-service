from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from rbac.models import PermissionRule, Role


class UserManager(BaseUserManager):
    def create_user(self, email: str, password: str | None = None, **extra_fields):
        if not email:
            raise ValueError('Email is required')

        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email: str, password: str, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')

        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    """Модель пользователя"""

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def has_perm(self, perm: str, obj: object | None = None) -> bool:
        return self.is_superuser

    def has_module_perms(self, app_label: str) -> bool:
        return self.is_superuser

    def __str__(self) -> str:
        return self.email

    def soft_delete(self):
        self.is_deleted = True
        self.is_active = False
        self.save()

    def get_rule(self, element_name: str) -> PermissionRule | None:
        """Возвращение правила доступа пользователя для указанного элемента"""

        return PermissionRule.objects.filter(
            role=self.role, element__name=element_name
        ).first()
