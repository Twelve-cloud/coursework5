from django.conf import settings
from datetime import datetime
from json import load
import pyEX as pyex
import os


client = pyex.Client(api_token=settings.PYEX_KEY, version='stable')


def read_companies() -> list:
    """
    read_companies: reads file with companies (name and symbol) and return list
    of these companies.
    """
    cur_path = os.path.dirname(__file__)

    with open(cur_path + '/symbols/symbols.json') as infile:
        companies = load(infile)

    return companies


def get_companies() -> dict:
    """
    get_companies: converts list of companies in one dict with structure:
    symbol -> name and returns it.
    """
    companies = {
        company['symbol']: company['name']
        for company in read_companies()
    }
    return companies


def get_companies_by_symbol(symbol: str) -> dict:
    """
    get_companies_by_symbol: converts list of companies in one dict with
    structure: symbol -> name for only companies which start with symbol
    and returns it.
    """
    symbol = symbol.upper()
    companies = {
        company['symbol']: company['name']
        for company in read_companies()
        if company['symbol'].startswith(symbol)
    }
    return companies


def get_company_data(symbol: str) -> dict:
    """
    get_company_data: returns company's data in dict. Company is chosen
    by symbol.
    """
    symbol = symbol.lower()
    company_data = client.company(symbol)
    company_data['logo'] = client.logo(symbol)
    return company_data


def get_company_shares(symbol: str) -> dict:
    """
    get_company_shares: returns data about company's shares. Company is chosen
    by symbol.
    """
    symbol = symbol.lower()
    shares_data = client.chart(symbol, timeframe='1y')

    chart = [
        {'date': shares['date'], 'close': shares['close']}
        for shares in shares_data if shares['close']
    ]

    last_updated = datetime.now().strftime('%b %-d %Y, %-I:%M %p')
    latest_price = chart[-1]['close']

    return {
        'chart': chart,
        'last_updated': last_updated,
        'latest_price': latest_price
    }
