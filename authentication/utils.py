import logging

from django.core.cache import InvalidCacheBackendError, cache
from django.utils import timezone

import jwt
import redis
from jwt import DecodeError, InvalidTokenError

logger = logging.getLogger(__name__)

DEFAULT_EXPIRE_TIMEOUT_SEC = 60 * 60


def add_token_to_blocklist(token: str) -> None:
    """Сохранение токена в Redis с ограниченным TTL"""

    if not token:
        return

    try:
        payload = jwt.decode(token, options={'verify_signature': False})
        exp_timestamp = payload.get('exp')
        now_timestamp = int(timezone.now().timestamp())
        ttl = max(exp_timestamp - now_timestamp, 0)

        if ttl > 0:
            cache.set(f'blocked_token:{token}', True, timeout=ttl)

    except (InvalidTokenError, DecodeError, KeyError, TypeError) as exc:
        logger.info(f'Blocking invalid JWT token {exc.__class__.__name__}')
        cache.set(f'blocked_token:{token}', True, timeout=DEFAULT_EXPIRE_TIMEOUT_SEC)


def is_token_blocked(token: str) -> bool:
    """Проверка нахождения токена в списке заблокированных"""

    if not token:
        return False

    try:
        return bool(cache.get(f'blocked_token:{token}'))
    except (redis.ConnectionError, redis.TimeoutError, InvalidCacheBackendError) as exc:
        logger.error(
            f'Redis error while checking token blacklist {exc.__class__.__name__}'
        )
        return False
