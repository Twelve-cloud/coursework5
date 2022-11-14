from shares.models import Broker, Order, Account
from rest_framework import serializers


class BrokerSerializer(serializers.ModelSerializer):
    orders = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    accounts = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = Broker
        fields = (
            'id',
            'name',
            'description',
            'type',
            'rate',
            'orders',
            'accounts',
        )
        read_only_fields = (
            'id',
            'orders',
            'accounts',
        )


class OrderSerializer(serializers.ModelSerializer):
    deal = serializers.PrimaryKeyRelatedField(
        read_only=True
    )

    class Meta:
        model = Order
        fields = (
            'id',
            'type',
            'status',
            'currency',
            'created_at',
            'description',
            'amount',
            'price',
            'broker',
            'user',
        )
        read_only_fields = (
            'id',
            'created_at',
        )


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'id',
            'balance',
            'currency',
            'broker',
            'user',
            'updated_at',
        )
        read_only_fields = (
            'id',
            'updated_at',
        )
