from rest_framework import serializers

from users.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'middle_name', 'password']
        extra_kwargs = {
            'middle_name': {'required': False, 'allow_null': True, 'allow_blank': True}
        }

    def create(self, validated_data: dict):
        return User.objects.create_user(**validated_data)
