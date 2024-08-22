import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import aiohttp
import json
from config import settings

class CurrencyConverter:
    def __init__(self) -> None:
        self.url = settings.template_exchange_rates_url
        self.date = settings.default_date
        self.apiVersion = settings.default_apiVersion
        self.endpoint = settings.default_endpoint
        self.currency_code = settings.default_currency_code

    def set_endpoint(self, endpoint) -> None:
        self.endpoint = endpoint
    
    def set_currency_code(self, currency_code) -> None:
        self.currency_code = currency_code

    async def build_api_url(self) -> str:
        return self.url.format(
            date=self.date,
            apiVersion=self.apiVersion,
            endpoint=self.endpoint
            )

    async def fetch_json_data(self, api_url: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                response = await resp.read()    
            response_data = json.loads(response.decode('utf-8'))
        return response_data

    async def get_all_currency_rates(self, endpoint) -> dict:
        api_url = await self.build_api_url()
        response_data = await self.fetch_json_data(api_url)
        return response_data[endpoint]

    def get_currency_sign(self, currency_code: str) -> str:
        currency_symbol = {
            "rub": "₽",
            "usd": "$",
            "eur": "€",
            "gbp": "£",
            "jpy": "¥",
            "cny": "¥",
            "aud": "A$",
            "cad": "C$",
            "chf": "₣",
            "dkk": "kr",
            "hkd": "HK$",
            "huf": "Ft",
            "inr": "₹",
            "nzd": "NZ$",
            "pln": "zł",
            "sgd": "S$",
            "thb": "฿",
            "try": "₺",
            "twd": "NT$",
            "zar": "R",
            "brl": "R$",
            "clp": "CLP$",
            "cop": "COP$",
            "mxn": "MX$",
            "pen": "S/.",
            "ars": "AR$",
            #...
        }
        return currency_symbol[currency_code]

    def get_single_currency_rate(self, 
        endpoint: str, currency_code: str) -> str:
        rates = asyncio.run(self.get_all_currency_rates(endpoint))
        return f"{rates[currency_code]:.2f}"

    def build_answer(self, message: str) -> str | None:
        if message.text.isdigit():
            money_amount = int(message.text)
            currency_rate = get_single_currency_rate(self.endpoint, self.currency_code),
            currency_symbol = get_currency_symbol(self.currency_code)
            answer = f"{money_amount * currency_rate} {currency_symbol}"
            return answer
        else: 
            return None