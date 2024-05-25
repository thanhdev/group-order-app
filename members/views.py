from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet

from members.serializers import MemberSerializer


class MemberViewSet(CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = MemberSerializer
