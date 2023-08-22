from rest_framework.exceptions import PermissionDenied, AuthenticationFailed
from jauth.services import get_payload_by_token
from django.shortcuts import get_object_or_404
from user.models import User


import wsgiref.util
wsgiref.util._hoppish = {
    'proxy-authenticate': 1,
    'proxy-authorization': 1, 'te': 1, 'trailers': 1, 'transfer-encoding': 1,
    'upgrade': 1
}.__contains__  # удалить


class JWTMiddleware:
    def __init__(self, next):
        self.next = next

    def __call__(self, request):
        access_token = request.headers.get('Authorization', None)
        access_token = request.COOKIES.get('access_token', None)  # удалить

        if access_token:
            payload = get_payload_by_token(access_token)

            if payload is None:
                raise AuthenticationFailed(detail='Unauthorized')

            request.user = get_object_or_404(User, pk=payload.get('sub'))

            if request.user.is_blocked:
                raise PermissionDenied(detail='User is blocked')

        response = self.next(request)
        response.setdefault('Connection', 'close')  # удалить
        return response
