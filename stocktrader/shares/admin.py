from django.contrib import admin
from shares.models import Broker, Order, Account, Stock, AccountHistory


class BrokerAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'rate', 'created_at')
    list_display_links = ('name', 'rate')
    search_fields = ('name', 'rate')
    list_filter = ('name', 'rate', 'created_at')
    ordering = ('name', 'rate', 'created_at')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('type', 'amount', 'company', 'created_at', 'broker', 'user')
    list_display_links = ('type', 'amount')
    search_fields = ('type', 'amount', 'company')
    list_filter = ('type', 'amount', 'company', 'created_at')
    ordering = ('type', 'amount', 'company', 'created_at')


class AccountAdmin(admin.ModelAdmin):
    list_display = ('balance', 'balance_with_shares', 'broker', 'user', 'updated_at')
    list_display_links = ('balance', 'balance_with_shares')
    search_fields = ('balance', 'balance_with_shares', 'updated_at')
    list_filter = ('balance', 'balance_with_shares', 'updated_at')
    ordering = ('balance', 'balance_with_shares', 'updated_at')


class StockAdmin(admin.ModelAdmin):
    list_display = ('company', 'amount', 'current_price', 'account')
    list_display_links = ('amount', 'company', 'current_price')
    search_fields = ('company', 'amount', 'current_price', 'account')
    list_filter = ('company', 'amount', 'current_price', 'account')
    ordering = ('company', 'amount', 'current_price', 'account')


class AccountHistoryAdmin(admin.ModelAdmin):
    list_display = ('balance', 'balance_with_shares', 'date', 'account')
    list_display_links = ('balance', 'balance_with_shares')
    search_fields = ('balance', 'balance_with_shares', 'date')
    list_filter = ('balance', 'balance_with_shares', 'date')
    ordering = ('balance', 'balance_with_shares', 'date')


admin.site.register(Broker, BrokerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(AccountHistory, AccountHistoryAdmin)
