from django.contrib import admin
from orders.models import Order, GroupOrder, OrderItem


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("name", "unit_price", "quantity", "order")
    list_filter = ("order",)

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "member", "group_order", "status", "is_paid")
    list_filter = ("status", "is_paid")
    search_fields = ("id", "member__username")
    readonly_fields = ("created_at",)

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(GroupOrder)
class GroupOrderAdmin(admin.ModelAdmin):
    list_display = ("id", "host_member", "status")
    list_filter = ("status",)
    search_fields = ("id", "host_member__username")
    readonly_fields = ("created_at",)

    def has_add_permission(self, request, obj=None):
        return False
