from rest_framework import serializers

from members.models import Member, Transaction


class MemberSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    def save(self, **kwargs):
        self.validated_data["username"] = self.validated_data["email"]
        user = Member.objects.create_user(**self.validated_data)
        return user

    class Meta:
        model = Member
        fields = (
            "id",
            "email",
            "name",
            "balance",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True}}


class TransactionSerializer(serializers.ModelSerializer):
    from_member = MemberSerializer()
    to_member = MemberSerializer()

    class Meta:
        model = Transaction
        fields = (
            "id",
            "from_member",
            "to_member",
            "amount",
            "type",
            "created_at",
        )
