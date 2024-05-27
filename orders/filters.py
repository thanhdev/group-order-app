import django_filters

from members.models import Member
from orders.models import Order, GroupOrder


class OrderFilter(django_filters.FilterSet):
    created_at = django_filters.DateTimeFromToRangeFilter()
    group_order = django_filters.ModelChoiceFilter(
        queryset=GroupOrder.objects.all()
    )
    member = django_filters.ModelChoiceFilter(queryset=Member.objects.all())

    class Meta:
        model = Order
        fields = ["is_paid", "created_at", "group_order", "member"]


class GroupOrderFilter(django_filters.FilterSet):
    created_at = django_filters.DateTimeFromToRangeFilter()
    host_member = django_filters.ModelChoiceFilter(
        queryset=Member.objects.all()
    )

    class Meta:
        model = GroupOrder
        fields = ["status", "created_at", "host_member"]
