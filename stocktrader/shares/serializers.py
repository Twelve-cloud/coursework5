from shares.models import Broker, Order, Deal, Account
from rest_framework import serializers


class BrokerSerializer(serializers.ModelSerializer):
    deals = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    accounts = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    orders = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = Broker
        fields = (
            'id',
            'name',
            'type',
            'rate',
            'deals',
            'accounts',
            'orders',
        )
        read_only_fields = (
            'id',
            'deals',
            'accounts',
            'orders',
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
            'amount',
            'price',
            'broker',
            'deal',
        )
        read_only_fields = (
            'id',
            'deal',
        )


class DealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deal
        fields = (
            'id',
            'created_at',
            'broker',
            'user',
            'order',
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
            'user'
        )
        read_only_fields = (
            'id',
        )
