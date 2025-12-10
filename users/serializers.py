from rest_framework import serializers

from .models import Role, User


class UserRoleUpdateSerializer(serializers.ModelSerializer):
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), source='role', write_only=True
    )

    class Meta:
        model = User
        fields = ['role_id']
