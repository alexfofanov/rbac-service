from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.jwt import create_access_token, create_refresh_token, decode_token
from authentication.models import BlacklistedToken
from authentication.serializers import LoginSerializer, RegisterSerializer


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
        token = request.data['refresh']
        payload = decode_token(token)
        if payload['type'] != 'refresh':
            return Response(
                {'detail': 'Invalid refresh'}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response({'access': create_access_token(payload['sub'])})


class LogoutAPIView(APIView):
    """Выход пользователя из системы"""

    def post(self, request: Request) -> Response:
        token = getattr(request, '_jwt_token', None)
        BlacklistedToken.objects.create(token=token)
        return Response({'detail': 'Logged out'})


class DeleteUserAPIView(APIView):
    """Удаление пользователя"""

    def delete(self, request: Request) -> Response:
        request._jwt_user.soft_delete()
        return Response({'detail': 'Soft deleted'})
