from rest_framework import serializers

from rbac.models import BusinessElement, PermissionRule, Role


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name', 'description')


class BusinessElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessElement
        fields = ('id', 'name', 'description')


class AccessRoleRuleSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), source='role', write_only=True
    )

    element = BusinessElementSerializer(read_only=True)
    element_id = serializers.PrimaryKeyRelatedField(
        queryset=BusinessElement.objects.all(), source='element', write_only=True
    )

    class Meta:
        model = PermissionRule
        fields = (
            'id',
            'role',
            'role_id',
            'element',
            'element_id',
            'read_permission',
            'read_all_permission',
            'create_permission',
            'update_permission',
            'update_all_permission',
            'delete_permission',
            'delete_all_permission',
        )

    def validate(self, attrs: dict) -> dict:
        role = attrs.get('role')
        element = attrs.get('element')

        if PermissionRule.objects.filter(role=role, element=element).exists():
            raise serializers.ValidationError(
                'Rule for this role and element already exists'
            )

        return attrs
