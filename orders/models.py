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


class OrderItem(models.Model):
    order = models.ForeignKey(
        "Order", related_name="items", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_cost(self):
        return self.unit_price * self.quantity


class Order(models.Model):
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="orders"
    )
    order_group = models.ForeignKey(
        GroupOrder, on_delete=models.CASCADE, related_name="orders"
    )
    status = models.CharField(
        max_length=255,
        choices=GroupOrderStatus.choices,
        default=GroupOrderStatus.DRAFT,
    )
    is_paid = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
