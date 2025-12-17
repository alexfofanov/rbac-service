from django.contrib.auth import authenticate

from rest_framework import serializers

from users.models import User

from authentication.jwt import decode_token
from authentication.utils import is_token_blocked


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


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs: dict) -> dict:
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError('Invalid credentials')

        attrs['user'] = user
        return attrs


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs: dict) -> dict:
        token = attrs['refresh']

        if is_token_blocked(token):
            raise serializers.ValidationError('Refresh token is blacklisted')

        payload = decode_token(token)
        if payload.get('type') != 'refresh':
            raise serializers.ValidationError('Invalid refresh token')

        attrs['payload'] = payload
        return attrs
