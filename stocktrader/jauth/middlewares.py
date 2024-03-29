from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from jauth.services import get_payload_by_token
from django.shortcuts import get_object_or_404
from user.models import User


class JWTMiddleware:
    def __init__(self, next):
        self.next = next

    def __call__(self, request):
        access_token = request.headers.get('Authorization', None)

        if access_token:
            payload = get_payload_by_token(access_token)

            if payload is None:
                raise AuthenticationFailed(detail='Unauthorized')

            request.user = get_object_or_404(User, pk=payload.get('sub'))

            if request.user.is_blocked:
                raise PermissionDenied(detail='User is blocked')

        response = self.next(request)
        return response
