from django.db import transaction
from rest_framework import serializers

from members.serializers import MemberSerializer
from orders.enums import OrderStatus
from orders.models import OrderItem, Order, GroupOrder


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            "id",
            "name",
            "quantity",
            "unit_price",
            "note",
        )


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    ordered_by = MemberSerializer(read_only=True, source="member")

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        member = self.context["request"].user
        with transaction.atomic():
            order = Order.objects.create(member=member, **validated_data)
            items = [
                OrderItem(order=order, **item_data) for item_data in items_data
            ]
            OrderItem.objects.bulk_create(items)
        return order

    class Meta:
        model = Order
        fields = (
            "id",
            "items",
            "group_order",
            "is_paid",
            "total_cost",
            "status",
            "ordered_by",
            "created_at",
        )


class GroupOrderSerializer(serializers.ModelSerializer):
    host_member = MemberSerializer(read_only=True)
    orders = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Order.objects.filter(status=OrderStatus.DRAFT).all(),
    )

    def create(self, validated_data):
        orders = validated_data.pop("orders")
        host_member = self.context["request"].user
        with transaction.atomic():
            group_order = GroupOrder.objects.create(
                host_member=host_member, **validated_data
            )
            for order in orders:
                order.group_order = group_order
                order.status = OrderStatus.IN_PROGRESS
            Order.objects.bulk_update(orders, ["group_order", "status"])
        return group_order

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["orders"] = OrderSerializer(instance.orders.all(), many=True).data
        return data

    class Meta:
        model = GroupOrder
        fields = (
            "id",
            "host_member",
            "orders",
            "actual_amount",
            "status",
            "created_at",
        )


class CompleteGroupOrderSerializer(serializers.Serializer):
    orders = serializers.PrimaryKeyRelatedField(
        many=True,
        allow_empty=True,
        queryset=Order.objects.all(),
    )
    discount = serializers.DecimalField(
        min_value=0., max_value=1., default=0., max_digits=5, decimal_places=2
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields["orders"].queryset = self.instance.orders.all()

    def save(self, **kwargs):
        to_complete_orders = self.validated_data.get("orders", [])
        discount = self.validated_data.get("discount", 0)
        self.instance.complete(to_complete_orders, discount)
        return self.instance
