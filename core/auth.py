import time

from rest_framework.authentication import BaseAuthentication

from members.models import Member


class Auth0UserBackend(BaseAuthentication):
    def authenticate(self, request):
        if data := request.session.get("user"):
            user_info = data["userinfo"]
            if user_info["exp"] < int(time.time()):
                return None
            user, _ = Member.objects.get_or_create(
                email=user_info["email"],
                defaults={
                    "name": user_info["name"],
                    "username": user_info["email"],
                },
            )
            if user.is_active:
                return user, None
        return None
