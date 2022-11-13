from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from jauth.services import get_payload_by_token
from django.shortcuts import get_object_or_404
from user.models import User


class JWTMiddleware:
    def __init__(self, next):
        self.next = next

    def __call__(self, request):
        access_token = request.COOKIES.get('access_token', None)

        if access_token:
            payload = get_payload_by_token(access_token)

            if payload is None:
                raise AuthenticationFailed(detail='Unauthorized')

            request.user = get_object_or_404(User, pk=payload.get('sub'))

            if request.user.is_blocked:
                raise PermissionDenied(detail='User is blocked')
                # If front-end will get HTTP_401_UNAUTHORIZED
                # It'll delete access token from cookie and
                # set refresh token to a cookie and request to
                # /auth/jwt/refresh to get new tokens

        response = self.next(request)
        return response
