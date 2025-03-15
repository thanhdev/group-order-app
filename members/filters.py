import django_filters
from django.db.models import Q

from members.models import Member, Transaction


class TransactionFilter(django_filters.FilterSet):
    created_at = django_filters.DateTimeFromToRangeFilter()
    member = django_filters.ModelChoiceFilter(queryset=Member.objects.all(), method="filter_by_member")

    class Meta:
        model = Transaction
        fields = ["from_member", "to_member", "member", "type", "created_at"]

    @staticmethod
    def filter_by_member(queryset, _, member):
        return queryset.filter(Q(from_member=member) | Q(to_member=member))
