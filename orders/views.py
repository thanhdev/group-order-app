from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from orders.enums import OrderStatus
from orders.filters import OrderFilter, GroupOrderFilter
from orders.models import Order, GroupOrder
from orders.serializers import OrderSerializer, GroupOrderSerializer


class OrderViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = OrderFilter

    def get_queryset(self):
        queryset = Order.objects.order_by("-created_at")
        if self.request.method not in SAFE_METHODS:
            member = self.request.user
            queryset = queryset.filter(member=member)
        return queryset

    @extend_schema(request=None)
    @action(detail=True, methods=["put"])
    def pay(self, request, pk=None):
        """
        Pay for an order. Only the host member of a group order can pay for it.
        """
        order = self.get_object()
        if order.status != OrderStatus.COMPLETED:
            raise ValidationError(
                {"detail": "This order is not ready for payment."}
            )
        elif order.group_order.host_member != request.user:
            raise PermissionDenied(
                {"detail": "You do not have permission to pay for this order."}
            )

        order.pay()
        serializer = self.get_serializer(order)
        return Response(serializer.data)


class GroupOrderViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    serializer_class = GroupOrderSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = GroupOrderFilter

    def get_queryset(self):
        queryset = GroupOrder.objects.order_by("-created_at")
        if self.request.method not in SAFE_METHODS:
            member = self.request.user
            queryset = queryset.filter(host_member=member)
        return queryset
