import json

import jwt
import requests
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework_jwt.authentication import (
    JSONWebTokenAuthentication as BaseJSONWebTokenAuthentication,
)


def jwt_get_username_from_payload_handler(payload):
    username = payload.get("sub").replace("|", ".")
    authenticate(remote_user=username)
    return username


def jwt_decode_token(token):
    header = jwt.get_unverified_header(token)
    jwks = requests.get(
        "https://{}/.well-known/jwks.json".format(settings.AUTH0_DOMAIN)
    ).json()
    public_key = None
    for jwk in jwks["keys"]:
        if jwk["kid"] == header["kid"]:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise Exception("Public key not found.")

    return jwt.decode(
        token,
        public_key,
        audience=settings.AUTH0_AUDIENCE,
        issuer=settings.AUTH0_ISSUER,
        algorithms=["RS256"],
    )


def get_token_auth_header(request):
    """Obtains the Access Token from the Authorization Header"""
    auth = request.META.get("HTTP_AUTHORIZATION", "")
    parts = auth.split()
    token = parts[1]

    return token


def get_userinfo(request):
    token = get_token_auth_header(request)
    endpoint = f"https://{settings.AUTH0_DOMAIN}/userinfo"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(endpoint, headers=headers)
    return response.json()


class JSONWebTokenAuthentication(BaseJSONWebTokenAuthentication):
    def authenticate(self, request):
        user_token = super().authenticate(request)
        if user_token is not None:
            user = user_token[0]
            if not user.email:  # first time login
                userinfo = get_userinfo(request)
                user.email = userinfo["email"]
                user.name = userinfo["nickname"]
                user.picture = userinfo["picture"]
                user.save()
        return user_token
