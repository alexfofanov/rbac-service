from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from rbac.models import BusinessElement, PermissionRule, Role
from rbac.serializers import (
    AccessRoleRuleSerializer,
    BusinessElementSerializer,
    RoleSerializer,
)


class RoleViewSet(viewsets.ModelViewSet):
    """CRUD-операции ролей"""

    element_name = 'rbac'

    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class BusinessElementViewSet(viewsets.ModelViewSet):
    """СRUD-операции бизнес-элементов"""

    element_name = 'rbac'

    queryset = BusinessElement.objects.all()
    serializer_class = BusinessElementSerializer


class PermissionRuleViewSet(viewsets.ModelViewSet):
    """CRUD-операции, фильтрация и получение правил доступа по роли"""

    element_name = 'rbac'

    queryset = PermissionRule.objects.select_related('role', 'element')
    serializer_class = AccessRoleRuleSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['role', 'element']
    search_fields = ['role__name', 'element__name']

    @action(detail=False, methods=['get'])
    def by_role(self, request: Request) -> Response:
        role_id = request.query_params.get('role_id')
        if not role_id:
            return Response(
                {'detail': 'role_id is required'}, status=status.HTTP_400_BAD_REQUEST
            )

        qs = self.get_queryset().filter(role_id=role_id)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
