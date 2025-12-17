from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.jwt import create_access_token, create_refresh_token
from authentication.serializers import (
    LoginSerializer,
    RefreshTokenSerializer,
    RegisterSerializer,
)
from authentication.utils import add_token_to_blocklist


class RegisterAPIView(APIView):
    """Регистрация нового пользователя"""

    def post(self, request: Request) -> Response:
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'id': user.id})


class LoginAPIView(APIView):
    """Вход пользователя в систему"""

    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        return Response(
            {
                'access': create_access_token(user.id),
                'refresh': create_refresh_token(user.id),
            },
            status=status.HTTP_200_OK,
        )


class RefreshAPIView(APIView):
    """Обновление токена"""

    def post(self, request: Request) -> Response:
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payload = serializer.validated_data['payload']
        token = serializer.validated_data['refresh']

        add_token_to_blocklist(token)
        # BlacklistedToken.objects.create(token=token)

        return Response(
            {'access': create_access_token(payload['sub'])},
            status=status.HTTP_200_OK,
        )


class LogoutAPIView(APIView):
    """Выход пользователя из системы"""

    def post(self, request: Request) -> Response:
        token = getattr(request, '_jwt_token', None)
        add_token_to_blocklist(token)
        # BlacklistedToken.objects.create(token=token)
        return Response({'detail': 'Logged out'})


class DeleteUserAPIView(APIView):
    """Удаление пользователя"""

    def delete(self, request: Request) -> Response:
        request._jwt_user.soft_delete()
        return Response({'detail': 'Soft deleted'})
