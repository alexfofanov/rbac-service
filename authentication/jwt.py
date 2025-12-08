from datetime import timedelta

from django.conf import settings
from django.utils import timezone

import jwt

ACCESS_EXPIRES_MIN = 10
REFRESH_EXPIRES_DAYS = 7


def create_access_token(user_id: int):
    """Создание JWT токена"""

    now = timezone.now()
    payload = {
        'sub': str(user_id),
        'type': 'access',
        'iat': now,
        'exp': now + timedelta(minutes=ACCESS_EXPIRES_MIN),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def create_refresh_token(user_id: int):
    """Создание refresh токена"""

    now = timezone.now()
    payload = {
        'sub': str(user_id),
        'type': 'refresh',
        'iat': now,
        'exp': now + timedelta(days=REFRESH_EXPIRES_DAYS),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')


def decode_token(token: str):
    """Расшифровка токена"""

    return jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
