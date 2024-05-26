from django.db import transaction
from rest_framework import serializers

from members.serializers import MemberSerializer
from orders.models import OrderItem, Order


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
            "order_group",
            "is_paid",
            "ordered_by",
            "created_at",
        )
        extra_kwargs = {
            "order_group": {"read_only": True},
            "is_paid": {"read_only": True},
        }
