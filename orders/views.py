from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from orders.filters import OrderFilter, GroupOrderFilter
from orders.models import Order, GroupOrder
from orders.serializers import (
    OrderSerializer,
    GroupOrderSerializer,
    CompleteGroupOrderSerializer,
    GroupOrderResponseSerializer,
)


class OrderViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = Order.objects.order_by("-created_at")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = OrderFilter

    def get_queryset(self):
        if self.request.method not in SAFE_METHODS:
            member = self.request.user
            self.queryset = self.queryset.filter(member=member)
        return self.queryset


class GroupOrderViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    queryset = GroupOrder.objects.order_by("-created_at")
    serializer_class = GroupOrderSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = GroupOrderFilter

    def get_queryset(self):
        if self.request.method not in SAFE_METHODS:
            member = self.request.user
            self.queryset = self.queryset.filter(host_member=member)
        return self.queryset

    def perform_destroy(self, instance):
        instance.cancel()

    @extend_schema(responses={201: GroupOrderResponseSerializer})
    def create(self, request, *args, **kwargs):
        """
        Create a group order.
        """
        return super().create(request, *args, **kwargs)

    @extend_schema(request=CompleteGroupOrderSerializer)
    @action(detail=True, methods=["put"])
    def complete(self, request, **kwargs):
        """
        Complete a group order. Only the host member can complete it.
        """
        group_order = self.get_object()
        if group_order.host_member != request.user:
            raise PermissionDenied(
                {
                    "detail": "You do not have permission to complete this "
                    "group order."
                }
            )

        serializer = CompleteGroupOrderSerializer(
            instance=group_order, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(self.get_serializer(group_order).data)
