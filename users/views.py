from urllib.request import Request

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import User
from users.serializers import UserRoleUpdateSerializer


class UserRoleViewSet(viewsets.GenericViewSet):
    element_name = 'rbac'

    queryset = User.objects.all()
    serializer_class = UserRoleUpdateSerializer

    @action(detail=True, methods=['patch'], url_path='update-role')
    def update_role(self, request: Request, pk: int | None = None):
        """Обновление роли пользователя"""

        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': 'role updated'}, status=status.HTTP_200_OK)
