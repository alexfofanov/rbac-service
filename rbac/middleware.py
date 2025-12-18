import json
import logging
from typing import Any, Callable

from django.http import HttpRequest as Request, JsonResponse
from django.utils.deprecation import MiddlewareMixin

from rest_framework import status

from users.models import User

from rbac.services import can

logger = logging.getLogger(__name__)


class RBACMiddleware(MiddlewareMixin):
    """Middleware для RBAC с поддержкой проверки владельца объекта"""

    skip_paths = [
        '/admin/',
        '/auth/',
        '/api/schema/',
        '/api/v1/auth/login',
        '/api/v1/auth/register',
        '/api/v1/auth/refresh',
        '/api/schema/',
        '/api/docs/',
    ]

    auth_only_paths = [
        '/api/v1/auth/logout',
        '/api/v1/auth/delete',
    ]

    method_action_map = {
        'GET': 'read',
        'POST': 'create',
        'PUT': 'update',
        'PATCH': 'update',
        'DELETE': 'delete',
    }

    def process_view(
        self, request: Request, view_func: Callable, view_args: list, view_kwargs: dict
    ) -> None | JsonResponse:
        path = request.path
        method = request.method.upper()
        logger.info(f'RBAC check: path={path}, method={method}')

        if any(path.startswith(skip) for skip in self.skip_paths):
            return None

        user = getattr(request, 'user', None)
        if not getattr(user, 'is_authenticated', False):
            return JsonResponse(
                {'detail': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if any(path.startswith(auth_path) for auth_path in self.auth_only_paths):
            return None

        resolver = getattr(request, 'resolver_match', None)
        view_class = getattr(getattr(resolver, 'func', None), 'cls', None)
        if not (view_class and hasattr(view_class, 'element_name')):
            logger.error(f'Element not found for path: {path}')
            return JsonResponse(
                {'detail': 'Element not found'}, status=status.HTTP_403_FORBIDDEN
            )

        element_name = view_class.element_name
        action = self.method_action_map.get(method)
        if not action:
            return None

        logger.debug(f'RBAC element={element_name}, action={action}')

        if action in ('read', 'create'):
            owner_id = None

            if action == 'read' and 'pk' in getattr(resolver, 'kwargs', {}):
                obj = self._get_object_for_view(view_class, request, resolver)
                owner_id = self._extract_owner_id(obj)

            elif action == 'create':
                data = self._get_request_data(request)
                owner_id = data.get('owner_id') or getattr(request.user, 'id', None)

            return self._deny_if_not_allowed(user, element_name, action, owner_id)

        obj = self._get_object_for_view(view_class, request, resolver)
        owner_id = self._extract_owner_id(obj)
        return self._deny_if_not_allowed(user, element_name, action, owner_id)

    @staticmethod
    def _get_object_for_view(
        view_class: Any, request: Request, resolver: Any
    ) -> Any | None:
        """Вызов get_object() у ViewSet для конкретного объекта"""

        try:
            view = view_class(**getattr(resolver.func, 'initkwargs', {}))
            view.request = request
            view.args = resolver.args
            view.kwargs = resolver.kwargs
            return view.get_object()
        except Exception as err:
            logger.error(f'RBAC get_object() error: {err}')
            return None

    @staticmethod
    def _extract_owner_id(obj: Any) -> int | None:
        """Получение owner_id или obj.owner.id"""

        if not obj:
            return None
        owner_id = getattr(obj, 'owner_id', None)
        if owner_id is not None:
            return owner_id
        owner = getattr(obj, 'owner', None)
        return getattr(owner, 'id', None) if owner else None

    @staticmethod
    def _deny_if_not_allowed(
        user: User, element_name: str, action: str, owner_id: int
    ) -> None | JsonResponse:
        """Проверка прав пользователя через"""

        allowed = can(user, element_name, action, obj_owner_id=owner_id)
        logger.info(
            f'RBAC: user={user.id}, element={element_name}, action={action}, owner={owner_id}, allowed={allowed}'
        )
        if not allowed:
            return JsonResponse(
                {'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN
            )
        return None

    @staticmethod
    def _get_request_data(request: Request) -> dict:
        """Получение данных из запроса"""

        if hasattr(request, 'data'):
            return request.data

        if request.POST:
            return request.POST

        content_type = request.META.get('CONTENT_TYPE', '')
        if 'application/json' in content_type:
            try:
                return json.loads(request.body or '{}')
            except Exception:
                return {}

        return {}
