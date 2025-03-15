import django_filters

from members.models import Member
from orders.models import Group, GroupOrder, Order


class OrderFilter(django_filters.FilterSet):
    created_at = django_filters.DateTimeFromToRangeFilter()
    group_order = django_filters.ModelChoiceFilter(queryset=GroupOrder.objects.all())
    member = django_filters.ModelChoiceFilter(queryset=Member.objects.all())

    class Meta:
        model = Order
        fields = ["is_paid", "created_at", "group_order", "member"]


class GroupOrderFilter(django_filters.FilterSet):
    created_at = django_filters.DateTimeFromToRangeFilter()
    host_member = django_filters.ModelChoiceFilter(queryset=Member.objects.all())

    class Meta:
        model = GroupOrder
        fields = ["status", "created_at", "host_member"]


class GroupFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")
    created_by = django_filters.ModelChoiceFilter(queryset=Member.objects.all())

    class Meta:
        model = Group
        fields = ["name", "created_by"]
