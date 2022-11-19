from shares.models import Broker, Order, Account, Stock, AccountHistory
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
    class Meta:
        model = Order
        fields = (
            'id',
            'type',
            'created_at',
            'description',
            'amount',
            'company',
            'broker',
            'user',
        )
        read_only_fields = (
            'id',
            'created_at',
        )


class AccountSerializer(serializers.ModelSerializer):
    shares = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    history = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = Account
        fields = (
            'id',
            'balance',
            'balance_with_shares',
            'broker',
            'user',
            'updated_at',
            'shares',
            'history',
        )
        read_only_fields = (
            'id',
            'updated_at',
            'shares',
            'history',
        )


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = (
            'id',
            'company',
            'amount'
            'purchase_price',
            'account',
        )
        read_only_fields = (
            'id',
        )


class AccountHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountHistory
        fields = (
            'id',
            'balance',
            'balance_with_shares',
            'date',
            'account',
        )
        read_only_fields = (
            'id',
            'date',
        )
