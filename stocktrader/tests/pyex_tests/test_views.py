from pyex.services import get_companies
from pyex.views import PyexViewSet
from rest_framework import status
import pytest


pytestmark = pytest.mark.django_db

company_data_view = PyexViewSet.as_view({'get': 'company_data'})
companies_view = PyexViewSet.as_view({'get': 'companies'})
company_shares_view = PyexViewSet.as_view({'get': 'company_shares'})
stock_latest_price_view = PyexViewSet.as_view({'get': 'stock_latest_price'})


class TestPyexViewSet:
    def test_company_data(self, api_factory, mocker):
        request = api_factory.get('/?symbol=aapl', '', format='json')
        get_company_data = mocker.MagicMock()
        mocker.patch('pyex.views.get_company_data', get_company_data)
        response = company_data_view(request)
        get_company_data.assert_called_once()
        assert response.status_code == status.HTTP_200_OK
        request = api_factory.get('', '', format='json')
        response = company_data_view(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_companies(self, api_factory, mocker):
        request = api_factory.get('/?symbol=aapl', '', format='json')
        get_companies_by_symbol = mocker.MagicMock()
        mocker.patch('pyex.views.get_companies_by_symbol', get_companies_by_symbol)
        response = companies_view(request)
        get_companies_by_symbol.assert_called_once()
        assert response.status_code == status.HTTP_200_OK
        request = api_factory.get('', '', format='json')
        response = companies_view(request)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == get_companies()

    def test_company_shares(self, api_factory, mocker):
        request = api_factory.get('/?symbol=aapl', '', format='json')
        get_company_shares = mocker.MagicMock(return_value=500)
        mocker.patch('pyex.views.get_company_shares', get_company_shares)
        response = company_shares_view(request)
        get_company_shares.assert_called_once()
        assert response.status_code == status.HTTP_200_OK
        request = api_factory.get('', '', format='json')
        response = company_shares_view(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_stock_latest_price_view(self, api_factory, mocker):
        request = api_factory.get('/?symbol=aapl', '', format='json')
        get_stock_latest_price = mocker.MagicMock()
        mocker.patch('pyex.views.get_stock_latest_price', get_stock_latest_price)
        response = stock_latest_price_view(request)
        get_stock_latest_price.assert_called_once()
        assert response.status_code == status.HTTP_200_OK
        request = api_factory.get('', '', format='json')
        response = stock_latest_price_view(request)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
