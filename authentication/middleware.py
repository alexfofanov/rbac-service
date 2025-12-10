import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin

from rest_framework.request import Request

import jwt

from authentication.models import BlacklistedToken

logger = logging.getLogger(__name__)


class JWTUserMiddleware(MiddlewareMixin):
    """Аутентификация с использованием JWT токена"""

    def process_request(self, request: Request) -> None:
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            logger.debug('No Authorization header found in the request.')
            return None

        if not auth_header.startswith('Bearer '):
            logger.debug(
                f'Authorization header present but not a Bearer token: {auth_header[:30]}...'
            )
            return None

        token = auth_header.split()[1]
        logger.debug(f'Received JWT token: {token[:20]}...')

        if BlacklistedToken.objects.filter(token=token).exists():
            logger.warning(f'Rejected blacklisted JWT token: {token[:20]}...')
            return None

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            logger.debug(f'JWT payload decoded successfully: {payload}')
        except jwt.InvalidTokenError as err:
            logger.warning(f'Invalid JWT token: {token[:20]}..., error: {err}')
            return None

        user_id = payload.get('sub')
        if not user_id:
            logger.warning(f"Missing 'sub' field in JWT payload: {payload}")
            return None

        User = get_user_model()  # noqa N806
        user = User.objects.filter(id=user_id).first()
        if not user:
            logger.warning(f'User not found for ID from JWT: {user_id}')
            return None

        request.user = user
        request._jwt_user = user
        request._jwt_token = token

        logger.info(f'User {user_id} successfully authenticated via JWT.')

        return None
