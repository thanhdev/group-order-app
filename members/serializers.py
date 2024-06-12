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
        extra_kwargs = {
            "password": {"write_only": True},
            "balance": {"read_only": True},
        }


class MemberUpdateSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        password = self.validated_data.pop("password", None)
        user = super().save(**kwargs)
        if password:
            user.set_password(password)
            user.save()
        return user

    class Meta:
        model = Member
        fields = (
            "name",
            "password",
        )


class TransactionSerializer(serializers.ModelSerializer):
    from_member = MemberSerializer(read_only=True)

    def validate_amount(self, value):
        user = self.context["request"].user
        if user.balance < value:
            raise serializers.ValidationError("Insufficient balance")
        return value

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
