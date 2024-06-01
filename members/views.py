from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from members.models import Member, Transaction
from members.serializers import (
    MemberSerializer,
    TransactionSerializer,
    TransactionResponseSerializer,
)


class MemberViewSet(
    ListModelMixin, RetrieveModelMixin, CreateModelMixin, GenericViewSet
):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new member.
        """
        return super().create(request, *args, **kwargs)

    @action(
        detail=False, methods=["get"], permission_classes=[IsAuthenticated]
    )
    def me(self, request, *args, **kwargs):
        """
        Get the authenticated member's profile.
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class TransactionViewSet(CreateModelMixin, ReadOnlyModelViewSet):
    queryset = Transaction.objects.all().order_by("-created_at")
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["from_member", "to_member", "type"]

    @extend_schema(
        responses={201: TransactionResponseSerializer},
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new transaction.
        """
        return super().create(request, *args, **kwargs)
