import django_filters
from members.models import Transaction


class TransactionFilter(django_filters.FilterSet):
    created_at = django_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Transaction
        fields = ["from_member", "to_member", "type", "created_at"]
