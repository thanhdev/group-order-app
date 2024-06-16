import time

from rest_framework.authentication import BaseAuthentication

from members.models import Member


def update_member(member: Member, userinfo: dict):
    """
    Update the user's information from the userinfo.
    """
    changed = False
    if member.name != userinfo["name"]:
        member.name = userinfo["name"]
        changed = True
    if member.picture != userinfo["picture"]:
        member.picture = userinfo["picture"]
        changed = True
    if changed:
        member.save()


class Auth0UserBackend(BaseAuthentication):
    def authenticate(self, request):
        if data := request.session.get("user"):
            user_info = data["userinfo"]
            if user_info["exp"] < int(time.time()):
                return None
            member, _ = Member.objects.get_or_create(
                email=user_info["email"],
                defaults={
                    "name": user_info["name"],
                    "username": user_info["email"],
                    "picture": user_info["picture"],
                },
            )
            if member.is_active:
                update_member(member, user_info)
                return member, None
        return None
