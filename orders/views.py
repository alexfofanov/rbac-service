from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from rbac.services import filter_queryset_by_owner

from orders.mock_data import MOCK_ORDERS


class MockOrderViewSet(ViewSet):
    element_name = 'order'

    def list(self, request: Request):
        user = self.request._jwt_user
        qs = MOCK_ORDERS
        rule = user.get_rule('order')
        qs = filter_queryset_by_owner(qs, user, rule)

        return Response(
            [
                {
                    'id': obj.id,
                    'product_name': obj.product_name,
                    'quantity': obj.quantity,
                    'owner_id': obj.owner_id,
                }
                for obj in qs
            ]
        )

    def retrieve(self, request: Request, pk: int | None = None):
        obj = self.get_object()
        return Response(
            {
                'id': obj.id,
                'product_name': obj.product_name,
                'quantity': obj.quantity,
                'owner_id': obj.owner_id,
            }
        )

    def create(self, request: Request):
        return Response({'detail': 'Order created'}, status=status.HTTP_201_CREATED)

    def update(self, request: Request, pk: int | None = None):
        obj = self.get_object()
        return Response({'detail': f'Order {obj.id} updated'})

    def destroy(self, request: Request, pk: int | None = None):
        obj = self.get_object()
        return Response({'detail': f'Order {obj.id} deleted'})

    def get_object(self):
        pk = int(self.kwargs.get('pk'))
        for obj in MOCK_ORDERS:
            if obj.id == pk:
                return obj
        raise Exception('Order not found')
