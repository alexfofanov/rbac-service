from django.core.management.base import BaseCommand

from users.models import User

from rbac.models import BusinessElement, PermissionRule, Role


class Command(BaseCommand):
    help = 'Заполняет RBAC модели'

    def handle(self, *args, **options):
        self.stdout.write('Создаем роли...')
        admin_role, _ = Role.objects.get_or_create(
            name='Admin', defaults={'description': 'Полный доступ'}
        )
        manager_role, _ = Role.objects.get_or_create(
            name='Manager', defaults={'description': 'Управление заказами'}
        )
        user_role, _ = Role.objects.get_or_create(
            name='User', defaults={'description': 'Обычный пользователь'}
        )

        self.stdout.write("Создаем бизнес-элемент 'order'...")
        order_element, _ = BusinessElement.objects.get_or_create(
            name='order', defaults={'description': 'Заказы'}
        )

        self.stdout.write("Создаем бизнес-элемент 'rbac'...")
        rbac_element, _ = BusinessElement.objects.get_or_create(
            name='rbac', defaults={'description': 'Управление ролями и правами'}
        )

        self.stdout.write('Создаем правила доступа для ролей...')
        PermissionRule.objects.get_or_create(
            role=admin_role,
            element=rbac_element,
            defaults={
                'read_permission': True,
                'read_all_permission': True,
                'create_permission': True,
                'update_permission': True,
                'update_all_permission': True,
                'delete_permission': True,
                'delete_all_permission': True,
            },
        )
        PermissionRule.objects.get_or_create(
            role=admin_role,
            element=order_element,
            defaults={
                'read_permission': True,
                'read_all_permission': True,
                'create_permission': True,
                'update_permission': True,
                'update_all_permission': True,
                'delete_permission': True,
                'delete_all_permission': True,
            },
        )
        PermissionRule.objects.get_or_create(
            role=manager_role,
            element=order_element,
            defaults={
                'read_permission': True,
                'read_all_permission': False,
                'create_permission': True,
                'update_permission': True,
                'update_all_permission': False,
                'delete_permission': False,
                'delete_all_permission': False,
            },
        )
        PermissionRule.objects.get_or_create(
            role=user_role,
            element=order_element,
            defaults={
                'read_permission': True,
                'read_all_permission': False,
                'create_permission': False,
                'update_permission': False,
                'update_all_permission': False,
                'delete_permission': False,
                'delete_all_permission': False,
            },
        )

        self.stdout.write('Создаем пользователей...')
        admin_user, _ = User.objects.get_or_create(
            email='admin@example.com',
            defaults={
                'first_name': 'Admin',
                'last_name': 'User',
                'role': admin_role,
            },
        )
        admin_user.set_password('admin123')
        admin_user.save()

        manager_user, _ = User.objects.get_or_create(
            email='manager@example.com',
            defaults={
                'first_name': 'Manager',
                'last_name': 'User',
                'role': manager_role,
            },
        )
        manager_user.set_password('manager123')
        manager_user.save()

        normal_user, _ = User.objects.get_or_create(
            email='user@example.com',
            defaults={
                'first_name': 'Normal',
                'last_name': 'User',
                'role': user_role,
            },
        )
        normal_user.set_password('user123')
        normal_user.save()

        if not User.objects.filter(is_superuser=True, is_staff=True).exists():
            User.objects.create_superuser(
                email='superuser@example.com',
                password='superuser123',
                first_name='Super',
                last_name='User',
            )
            self.stdout.write(
                self.style.SUCCESS(
                    'Superuser создан: superuser@example.com / superuser123'
                )
            )

        self.stdout.write(
            self.style.SUCCESS('Тестовые данные и заказы успешно созданы!')
        )
