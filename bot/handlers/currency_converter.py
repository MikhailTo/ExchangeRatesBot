import json
import aiohttp
from fluent.runtime.types import fluent_number

from config import settings

class CurrencyConverter:

    def __init__(self, l10n) -> None:
        self.l10n = l10n
        self.url = settings.template_exchange_rates_url
        self.date = settings.default_date
        self.apiVersion = settings.default_apiVersion

    user_data = {
            "chosen_currency_code_from": settings.default_currency_code_from,
            "chosen_currency_code_to": settings.default_currency_code_to
        }

    def set_currency_code_from(self, currency_code) -> None:
        self.user_data["chosen_currency_code_from"] = currency_code
        print(f'chosen_currency_code_from: {self.user_data["chosen_currency_code_from"]}')

    def set_currency_code_to(self, currency_code) -> None:
        self.user_data["chosen_currency_to"] = currency_code
        print(f'chosen_currency_code_to: {self.user_data["chosen_currency_code_to"]}')

    async def build_api_url(self) -> str:
        return self.url.format(
            date=self.date,
            apiVersion=self.apiVersion,
            endpoint=self.user_data["chosen_currency_code_from"]
            )

    async def fetch_json_data(self, api_url: str) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as resp:
                response = await resp.read()
            response_data = json.loads(response.decode('utf-8'))
        return response_data

    async def get_all_currency_rates(self, currency_code_from) -> dict:
        api_url = await self.build_api_url()
        response_data = await self.fetch_json_data(api_url)
        return response_data[currency_code_from]
 
    async def get_single_currency_rate(self,
        currency_code_from: str, currency_code_to: str) -> float:
        rates = await self.get_all_currency_rates(currency_code_from)
        return rates[currency_code_to]

    async def build_answer(self, message: str) -> str | None:
        if message.text.lstrip('+-').isdigit():
            money_amount = int(message.text)
        else:
            return None

        currency_rate = await self.get_single_currency_rate(
            self.user_data["chosen_currency_code_from"],
            self.user_data["chosen_currency_code_to"]
            )

        counted_currency = round(money_amount * float(currency_rate), 2)

        currency_number_from = fluent_number(
            money_amount, style="currency",
            currency=self.user_data["chosen_currency_code_from"].upper())

        currency_number_to = fluent_number(
            counted_currency, style="currency",
            currency=self.user_data["chosen_currency_code_to"].upper())

        currency = self.l10n.format_value("currency", {
            "chosen_currency_code_from": self.user_data["chosen_currency_code_from"].upper(),
            "chosen_currency_code_to": self.user_data["chosen_currency_code_to"].upper(),
            "currency_number_from": currency_number_from,
            "currency_number_to": currency_number_to})

        return currency

    