from drf_spectacular.utils import extend_schema
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from members.models import Member, Transaction
from members.serializers import (
    MemberSerializer,
    TransactionSerializer,
    TransactionResponseSerializer,
    MemberUpdateSerializer,
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


class MemberMeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=MemberSerializer)
    def get(self, request, *args, **kwargs):
        """
        Get the authenticated member's profile.
        """
        return Response(MemberSerializer(request.user).data)

    @extend_schema(request=MemberUpdateSerializer, responses=MemberSerializer)
    def patch(self, request, *args, **kwargs):
        """
        Update the authenticated member's profile.
        """
        serializer = MemberUpdateSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(MemberSerializer(user).data)


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
