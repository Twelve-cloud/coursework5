from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
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
        )
        read_only_fields = (
            'id',
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
