from jauth.services import (
    set_tokens_to_cookie, get_payload_by_token, verify_user, generate_token
)
from jauth.serializers import SignInSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import redirect
from rest_framework import viewsets
from rest_framework import status
from user.models import User


class AuthViewSet(viewsets.GenericViewSet):
    @action(detail=False, methods=['post'], serializer_class=SignInSerializer)
    def sign_in(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        set_tokens_to_cookie(response, serializer.validated_data['id'])
        access_token = generate_token(type='access', user_id=serializer.validated_data['id'])
        refresh_token = generate_token(type='refresh', user_id=serializer.validated_data['id'])
        response.data['access_token'] = access_token
        response.data['refresh_token'] = refresh_token
        response.data['user_id'] = serializer.validated_data['id']
        return response

    @action(detail=False, methods=['get'])
    def refresh(self, request):
        refresh_token = request.COOKIES.get('refresh_token', None)
        payload = get_payload_by_token(refresh_token)

        if payload is None:
            return Response(
                data={'Refresh Token': 'Expired'},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.user = User.objects.get(pk=payload.get('sub'))

        response = Response(
            data={'Tokens': 'OK'},
            status=status.HTTP_200_OK
        )
        set_tokens_to_cookie(response, request.user.id)

        return response

    @action(detail=False, methods=['get'])
    def verify_email(self, request):
        user_token = request.query_params.get('token', None)
        payload = get_payload_by_token(user_token)

        if payload is None:
            return Response(
                data={'Error': 'Verify link'},
                status=status.HTTP_400_BAD_REQUEST
            )

        email = payload.get('sub')
        verify_user(email)

        return redirect('http://localhost:5000/sign-in')
