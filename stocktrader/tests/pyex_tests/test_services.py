from pyex.services import (
    read_companies, get_companies, get_companies_by_symbol,
    get_company_data, get_company_shares, get_stock_latest_price
)
from pyex.services import client
import pytest


pytestmark = pytest.mark.django_db


class TestPyexServices:
    def test_read_companies(self):
        assert read_companies() == eval(open('pyex/symbols/symbols.json').read())

    def test_get_companies(self):
        assert get_companies() == {
            company['symbol']: company['name']
            for company in read_companies()
        }

    def test_get_companies_by_symbol(self):
        apple = get_companies_by_symbol('aapl')
        assert 'AAPL' in apple

    def test_get_company_data(self, mocker):
        company = mocker.MagicMock(return_value={})
        logo = mocker.MagicMock(return_value='Apple logo')
        mocker.patch.object(client, 'company', company)
        mocker.patch.object(client, 'logo', logo)
        result = get_company_data('aapl')
        company.assert_called_once()
        logo.assert_called_once()
        assert result == {'logo': 'Apple logo'}

    def test_get_comapany_shares(self, mocker):
        chart = mocker.MagicMock(return_value=[{'date': 'current', 'close': '150'}])
        mocker.patch.object(client, 'chart', chart)
        result = get_company_shares('aapl')
        chart.assert_called_once()
        assert result['latest_price'] == '150'
        assert get_company_shares(None) is None

    def test_get_stock_latest_price(self, mocker):
        quote = mocker.MagicMock(return_value={'latestPrice': '150'})
        mocker.patch.object(client, 'quote', quote)
        result = get_stock_latest_price('aapl')
        quote.assert_called_once()
        assert result == '150'
        assert get_stock_latest_price(None) is None
