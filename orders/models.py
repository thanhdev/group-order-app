from django.db import models

from members.models import Member
from orders.enums import GroupOrderStatus


class GroupOrder(models.Model):
    host_member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="hosted_group_orders"
    )
    actual_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    status = models.CharField(
        max_length=50,
        choices=GroupOrderStatus.choices,
        default=GroupOrderStatus.DRAFT,
    )


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
        Member, on_delete=models.CASCADE, related_name="orders"
    )
    order_group = models.ForeignKey(
        GroupOrder,
        on_delete=models.CASCADE,
        related_name="orders",
        null=True,
        blank=True,
    )
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def status(self) -> GroupOrderStatus:
        if self.order_group:
            return GroupOrderStatus(self.order_group.status)
        return GroupOrderStatus.DRAFT
