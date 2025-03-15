from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin)
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from orders.filters import GroupFilter, GroupOrderFilter, OrderFilter
from orders.models import Group, GroupOrder, Order
from orders.serializers import (CompleteGroupOrderSerializer,
                                GroupOrderResponseSerializer,
                                GroupOrderSerializer, GroupSerializer,
                                OrderSerializer)


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
            raise PermissionDenied({"detail": "You do not have permission to complete this " "group order."})

        serializer = CompleteGroupOrderSerializer(instance=group_order, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(self.get_serializer(group_order).data)


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.order_by("-created_at")
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = GroupFilter

    @action(detail=True, methods=["post"], serializer_class=None)
    def join(self, request, **kwargs):
        """
        Join a group.
        """
        group = self.get_object()
        if group.members.filter(pk=request.user.pk).exists():
            raise ValidationError({"detail": "You are already a member of this group."})

        group.members.add(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"], serializer_class=None)
    def leave(self, request, **kwargs):
        """
        Leave a group.
        """
        group = self.get_object()
        if not group.members.filter(pk=request.user.pk).exists():
            raise ValidationError({"detail": "You are not a member of this group."})

        group.members.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"], serializer_class=None)
    def priority(self, request, **kwargs):
        """
        Update your priority in a group.
        """
        group = self.get_object()
        priority = request.data.get("priority")
        if not priority:
            raise ValidationError({"priority": "This field is required."})
        try:
            priority = int(priority)
        except ValueError:
            raise ValidationError({"priority": "A valid integer is required."})

        group_member = group.groupmember_set.get(member=request.user)
        group_member.priority = priority
        group_member.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
