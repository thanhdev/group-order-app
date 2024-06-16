from urllib.parse import quote_plus, urlencode

from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
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

oauth = OAuth()
oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
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


def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    return redirect(request.build_absolute_uri(reverse("index")))


def login(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("oauth0-callback"))
    )


def logout(request):
    request.session.clear()

    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )
