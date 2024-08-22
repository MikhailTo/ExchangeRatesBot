import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import asyncio
import aiohttp
from bot.config import settings






class CurrencyConverter:
    def __init__(self, l10n) -> None:
        self.l10n = l10n
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
    
    def get_currency_symbol(self, currency_code):
        return self.l10n.format_value(f"currency-symbols.{currency_code}")

    def get_single_currency_rate(self,
        endpoint: str, currency_code: str) -> str:
        rates = asyncio.run(self.get_all_currency_rates(endpoint))
        return f"{rates[currency_code]:.2f}"

    def build_answer(self, message: str) -> str | None:
        if message.text.isdigit():
            money_amount = int(message.text)
            currency_rate = self.get_single_currency_rate(self.endpoint, self.currency_code),
            currency_symbol = self.get_currency_symbol(currency_symbol)
            answer = f"{money_amount * currency_rate} {currency_symbol}"
            return answer
        else:
            return None