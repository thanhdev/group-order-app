from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from members.models import Member
from members.serializers import MemberSerializer


class MemberViewSet(CreateModelMixin, GenericViewSet):
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
