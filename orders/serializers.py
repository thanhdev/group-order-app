from django.db import transaction
from rest_framework import serializers

from members.serializers import MemberSerializer
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
            "status",
            "ordered_by",
            "created_at",
        )
        extra_kwargs = {
            "group_order": {"read_only": True},
            "is_paid": {"read_only": True},
        }


class GroupOrderSerializer(serializers.ModelSerializer):
    host_member = MemberSerializer(read_only=True)
    orders = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Order.objects.filter(group_order=None).all()
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
            Order.objects.bulk_update(orders, ["group_order"])
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
        read_ony_fields = (
            "host_member",
            "actual_amount",
            "status",
            "created_at",
        )
