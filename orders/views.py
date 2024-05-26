from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS

from orders.filters import OrderFilter
from orders.models import Order
from orders.serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = OrderFilter

    def get_queryset(self):
        queryset = Order.objects.order_by("-created_at")
        if self.request.method not in SAFE_METHODS:
            member = self.request.user
            queryset = queryset.filter(member=member)
        return queryset
