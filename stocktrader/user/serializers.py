from rest_framework import serializers
from user.models import User


class BasicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'password',
            'first_name',
            'last_name',
            'image',
        )
        read_only_fields = (
            'id',
        )


class FullUserSerializer(BasicUserSerializer):
    deals = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    accounts = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'password',
            'first_name',
            'last_name',
            'image',
            'is_staff',
            'is_active',
            'is_blocked',
            'last_login',
            'date_joined',
        )
        read_only_fields = (
            'id',
            'is_active',
            'last_login',
            'date_joined',
        )
