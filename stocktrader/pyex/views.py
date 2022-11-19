from pyex.services import (
    get_company_data, get_companies, get_companies_by_symbol,
    get_company_shares, get_stock_latest_price
)
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status


class PyexViewSet(viewsets.GenericViewSet):
    @action(detail=False, methods=['get'])
    def company_data(self, request):
        symbol = request.query_params.get('symbol', None)

        if symbol:
            return Response(
                data=get_company_data(symbol),
                status=status.HTTP_200_OK
            )

        return Response(
            data='Error: Specify company',
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['get'])
    def companies(self, request):
        symbol = request.query_params.get('symbol', None)

        if symbol:
            return Response(
                data=get_companies_by_symbol(symbol),
                status=status.HTTP_200_OK
            )

        return Response(
            data=get_companies(),
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'])
    def company_shares(self, request):
        symbol = request.query_params.get('symbol', None)

        company_shares = get_company_shares(symbol)

        if company_shares and symbol:
            return Response(
                data=company_shares,
                status=status.HTTP_200_OK
            )

        return Response(
            data='Error: Specify company',
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['get'])
    def stock_latest_price(self, request):
        symbol = request.query_params.get('symbol', None)

        latest_price = get_stock_latest_price(symbol)

        if symbol and latest_price:
            return Response(data=latest_price, status=status.HTTP_200_OK)

        return Response(
            data='Error: Specify company',
            status=status.HTTP_400_BAD_REQUEST
        )
