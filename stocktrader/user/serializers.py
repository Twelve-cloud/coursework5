from rest_framework import serializers
from user.models import User


class BasicUserSerializer(serializers.ModelSerializer):
    orders = serializers.PrimaryKeyRelatedField(
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
            'orders',
            'accounts',
            'follows',
            'followers'
        )
        read_only_fields = (
            'id',
            'orders',
            'accounts',
            'follows',
            'followers'
        )

    def create(self, validated_data):
        validated_data['is_active'] = False
        return self.Meta.model.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class FullUserSerializer(BasicUserSerializer):
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
            'orders',
            'accounts',
            'follows',
            'followers',
            'is_blocked',
            'is_active',
            'is_staff',
            'date_joined',
            'last_login'
        )
        read_only_fields = (
            'id',
            'orders',
            'accounts',
            'follows',
            'followers',
            'is_blocked',
            'is_active',
            'is_staff',
            'date_joined',
            'last_login'
        )
