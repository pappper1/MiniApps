import requests
from datetime import datetime, timedelta


class CurrencyParser:
    def __init__(self, from_currency: str, to_currency: str):
        self.end_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        self.start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        self.headers =  {
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Accept': 'application/json, text/plain, */*',
            'Referer': '',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'sec-ch-ua-platform': '"Windows"',
        }
        self.params = {
            'base': from_currency,
            'quote': to_currency,
            'data_type': 'chart',
            'start_date': self.start_date,
            'end_date': self.end_date,
        }


    def get_exchange_rate(self) -> float:
        response = requests.get('https://fxds-public-exchange-rates-api.oanda.com/cc-api/currencies',
                                params=self.params, headers=self.headers).json()
        return float(response['response'][0]['average_bid'])