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
            "picture",
            "password",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "balance": {"read_only": True},
        }


class MemberUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ("name", "picture")


class TransactionSerializer(serializers.ModelSerializer):
    from_member = MemberSerializer(read_only=True)

    def validate_amount(self, value):
        user = self.context["request"].user
        if value <= 0:
            raise serializers.ValidationError("Invalid amount.")
        return value

    def validate_to_member(self, member):
        if member == self.context["request"].user:
            raise serializers.ValidationError("Cannot transfer to yourself.")
        return member

    def create(self, validated_data):
        from_member = self.context["request"].user
        transaction = Transaction.objects.create(
            from_member=from_member,
            type=Transaction.Type.TRANSFER,
            **validated_data,
        )
        return transaction

    def to_representation(self, instance):
        instance.refresh_from_db()
        data = super().to_representation(instance)
        data["to_member"] = MemberSerializer(instance.to_member).data
        return data

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
        read_only_fields = ("type",)


class TransactionResponseSerializer(TransactionSerializer):
    to_member = MemberSerializer(read_only=True)
