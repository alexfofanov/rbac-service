from django.contrib.auth import authenticate

from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.jwt import create_access_token, create_refresh_token, decode_token
from authentication.models import BlacklistedToken
from authentication.serializers import RegisterSerializer


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
        email = request.data['email']
        password = request.data['password']

        user = authenticate(email=email, password=password)
        if not user:
            return Response({'detail': 'Invalid credentials'}, status=400)

        return Response(
            {
                'access': create_access_token(user.id),
                'refresh': create_refresh_token(user.id),
            }
        )


class RefreshAPIView(APIView):
    """Обновление токена"""

    def post(self, request: Request) -> Response:
        token = request.data['refresh']
        payload = decode_token(token)
        if payload['type'] != 'refresh':
            return Response({'detail': 'Invalid refresh'}, status=400)

        return Response({'access': create_access_token(payload['sub'])})


class LogoutAPIView(APIView):
    """Выход пользователя из системы"""

    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        token = request.auth
        BlacklistedToken.objects.create(token=token)
        return Response({'detail': 'Logged out'})


class DeleteUserAPIView(APIView):
    """Удаление пользователя"""

    permission_classes = [IsAuthenticated]

    def delete(self, request: Request) -> Response:
        request.user.soft_delete()
        return Response({'detail': 'Soft deleted'})
