from django.contrib import admin

from core.admins import ReadOnlyModelAdmin
from orders.models import Order, GroupOrder, OrderItem


@admin.register(OrderItem)
class OrderItemAdmin(ReadOnlyModelAdmin):
    list_display = ("name", "unit_price", "quantity", "order")
    list_filter = ("order",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ("name", "unit_price", "quantity", "note")
    readonly_fields = ("name", "unit_price", "quantity", "note")


@admin.register(Order)
class OrderAdmin(ReadOnlyModelAdmin):
    list_display = ("id", "member", "group_order", "status", "is_paid")
    list_filter = ("status", "is_paid")
    search_fields = ("id", "member__username")
    readonly_fields = ("created_at",)
    inlines = [OrderItemInline]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class OrderInline(admin.TabularInline):
    model = Order
    extra = 0
    fields = ("id", "member", "status", "is_paid")
    readonly_fields = ("id", "member", "status", "is_paid")


@admin.register(GroupOrder)
class GroupOrderAdmin(ReadOnlyModelAdmin):
    list_display = ("id", "host_member", "status")
    list_filter = ("status",)
    search_fields = ("id", "host_member__username")
    readonly_fields = ("created_at",)
    inlines = [OrderInline]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
