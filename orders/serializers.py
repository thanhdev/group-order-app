from django.db import transaction
from rest_framework import serializers

from members.models import Member
from members.serializers import MemberSerializer
from orders.enums import OrderStatus
from orders.models import Group, GroupMember, GroupOrder, Order, OrderItem


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
    created_by = MemberSerializer(read_only=True)
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        required=False,
    )
    on_behalf_of = serializers.PrimaryKeyRelatedField(
        queryset=Member.objects.all(),
        write_only=True,
        required=False,
    )

    def validate_group(self, group):
        member = self.context["request"].user
        if not group.members.filter(pk=member.pk).exists():
            raise serializers.ValidationError("You are not a member of this group.")
        return group

    def validate(self, attrs):
        if on_behalf_of := attrs.get("on_behalf_of"):
            if not (group := attrs.get("group")):
                raise serializers.ValidationError("The group is required when on_behalf_of is provided.")
            if not GroupMember.objects.filter(group=group, member=on_behalf_of).exists():
                raise serializers.ValidationError("The on_behalf_of member is not a member of the group.")
        return attrs

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        on_behalf_of = validated_data.pop("on_behalf_of", None)

        request_user = self.context["request"].user
        if on_behalf_of is not None:
            member = on_behalf_of
            created_by = request_user
        else:
            member = created_by = request_user

        with transaction.atomic():
            order = Order.objects.create(member=member, created_by=created_by, **validated_data)
            items = [OrderItem(order=order, **item_data) for item_data in items_data]
            OrderItem.objects.bulk_create(items)
        return order

    class Meta:
        model = Order
        fields = (
            "id",
            "items",
            "group",
            "group_order",
            "is_paid",
            "total_cost",
            "status",
            "ordered_by",
            "created_at",
            "created_by",
            "on_behalf_of",
        )


class GroupOrderSerializer(serializers.ModelSerializer):
    host_member = MemberSerializer(read_only=True)
    orders = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Order.objects.filter(status=OrderStatus.DRAFT).all(),
    )
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all(),
        required=False,
    )

    def validate_group(self, group):
        member = self.context["request"].user
        if not group.members.filter(pk=member.pk).exists():
            raise serializers.ValidationError("You are not a member of this group.")
        return group

    def validate(self, attrs):
        orders = attrs.get("orders", [])
        for order in orders:
            if order.group != attrs.get("group"):
                raise serializers.ValidationError("All orders must belong to the same group.")
        return attrs

    def create(self, validated_data):
        orders = validated_data.pop("orders")
        host_member = self.context["request"].user
        with transaction.atomic():
            group_order = GroupOrder.objects.create(host_member=host_member, **validated_data)
            for order in orders:
                order.group_order = group_order
                order.status = OrderStatus.IN_PROGRESS
            Order.objects.bulk_update(orders, ["group_order", "status"])
        return group_order

    def to_representation(self, instance):
        instance.refresh_from_db()
        data = super().to_representation(instance)
        data["orders"] = OrderSerializer(instance.orders.all(), many=True).data
        return data

    class Meta:
        model = GroupOrder
        fields = (
            "id",
            "group",
            "host_member",
            "orders",
            "actual_amount",
            "status",
            "created_at",
        )


class GroupOrderResponseSerializer(GroupOrderSerializer):
    orders = OrderSerializer(many=True)


class CompleteGroupOrderSerializer(serializers.Serializer):
    instance: GroupOrder
    orders = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Order.objects.all(),
    )
    actual_amount = serializers.DecimalField(max_digits=10, decimal_places=1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields["orders"].queryset = self.instance.orders.all()

    def save(self, **kwargs):
        to_complete_orders = self.validated_data.get("orders", [])
        actual_amount = self.validated_data["actual_amount"]
        self.instance.complete(to_complete_orders, actual_amount)
        return self.instance


class GroupSerializer(serializers.ModelSerializer):
    members_count = serializers.SerializerMethodField()
    joined = serializers.SerializerMethodField()
    created_by = MemberSerializer(read_only=True)
    priority = serializers.SerializerMethodField()

    @staticmethod
    def get_members_count(instance):
        return instance.members.count()

    def get_joined(self, instance):
        member = self.context["request"].user
        return instance.members.filter(pk=member.pk).exists()

    def get_priority(self, instance):
        member = self.context["request"].user
        try:
            return GroupMember.objects.get(group=instance, member=member).priority
        except GroupMember.DoesNotExist:
            return None

    def create(self, validated_data):
        member = self.context["request"].user
        with transaction.atomic():
            group = Group.objects.create(created_by=member, **validated_data)
            GroupMember.objects.create(group=group, member=member, is_admin=True)
        return group

    class Meta:
        model = Group
        fields = [
            "id",
            "name",
            "description",
            "logo",
            "created_at",
            "created_by",
            "members_count",
            "joined",
            "priority",
        ]
