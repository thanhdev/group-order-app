from django.db import models

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

    def pay(self):
        self.is_paid = True
        self.save()
