from django.contrib.auth.models import User

from rest_framework import serializers


class MemberSerializer(serializers.ModelSerializer):
    def save(self, **kwargs):
        user = User.objects.create_user(**self.validated_data)
        return user

    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )
        extra_kwargs = {"password": {"write_only": True, "required": True}}
