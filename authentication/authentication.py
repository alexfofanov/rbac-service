from django.conf import settings

from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request

import jwt

from .models import BlacklistedToken


class JWTAuthentication(BaseAuthentication):
    """Аутентификация пользователя на основе JWT-токена"""

    keyword = 'Bearer'

    def authenticate(self, request: Request):
        header = request.headers.get('Authorization')
        if not header:
            return None

        parts = header.split()
        if len(parts) != 2 or parts[0] != self.keyword:
            return None

        token = parts[1]

        if BlacklistedToken.objects.filter(token=token).exists():
            raise exceptions.AuthenticationFailed('Token blacklisted')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError as err:
            raise exceptions.AuthenticationFailed('Token has expired') from err
        except jwt.InvalidTokenError as err:
            raise exceptions.AuthenticationFailed('Invalid token') from err

        user_id = payload.get('sub')
        if not user_id:
            raise exceptions.AuthenticationFailed('Invalid payload')

        from django.contrib.auth import get_user_model

        User = get_user_model()  # noqa: N806
        user = User.objects.filter(id=int(user_id)).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        return user, token
