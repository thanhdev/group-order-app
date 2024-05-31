from typing import Sequence

from django.db import models, transaction
from django.utils.functional import cached_property

from members.models import Member
from orders.enums import GroupOrderStatus, OrderStatus


class GroupOrder(models.Model):
    host_member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="hosted_group_orders",
        editable=False,
    )
    actual_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, editable=False
    )
    status = models.CharField(
        max_length=50,
        choices=GroupOrderStatus.choices,
        default=GroupOrderStatus.IN_PROGRESS,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def cancel(self):
        with transaction.atomic():
            self.status = GroupOrderStatus.CANCELLED
            self.save()
            orders = self.orders.all()
            for order in orders:
                order.group_order = None
            Order.objects.bulk_update(orders, ["group_order"])

    def complete(self, to_complete_orders: Sequence["Order"], discount: float):
        actual_amount = 0
        all_orders = self.orders.all()
        with transaction.atomic():
            # update order status and member balance
            for order in all_orders:
                if order not in to_complete_orders:
                    order.status = OrderStatus.CANCELLED
                else:
                    order.status = OrderStatus.COMPLETED
                    order.is_paid = True
                    total_cost = order.total_cost * (1 - discount)
                    actual_amount += total_cost
                    order.member.balance -= total_cost
                    self.host_member.balance += total_cost
            members = [order.member for order in all_orders]
            members.append(self.host_member)
            Member.objects.bulk_update(members, ["balance"])
            Order.objects.bulk_update(all_orders, ["status"])

            # update group order status
            self.status = GroupOrderStatus.COMPLETED
            self.actual_amount = actual_amount
            self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(
        "Order", related_name="items", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    unit_price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)
    note = models.TextField(blank=True, null=True)

    def get_cost(self):
        return self.unit_price * self.quantity


class Order(models.Model):
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="orders", editable=False
    )
    group_order = models.ForeignKey(
        GroupOrder,
        on_delete=models.SET_NULL,
        related_name="orders",
        null=True,
        blank=True,
        editable=False,  # set when the group_order is created
    )
    status = models.CharField(
        max_length=50,
        choices=OrderStatus.choices,
        default=OrderStatus.DRAFT,
        editable=False,
    )
    # set to True when the order is paid
    is_paid = models.BooleanField(default=False, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @cached_property
    def total_cost(self):
        return (
            self.items.aggregate(
                total_cost=models.Sum(
                    models.F("unit_price") * models.F("quantity"),
                    output_field=models.IntegerField(),
                )
            )["total_cost"]
            or 0
        )
