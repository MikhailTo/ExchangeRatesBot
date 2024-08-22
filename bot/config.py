from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: SecretStr
    
    # Настройки для API курсов валют
    default_date: str ="latest"
    default_apiVersion: str  = "v1"
    default_endpoint: str = "usd"
    default_currency_code: str = "rub"
    template_exchange_rates_url: str = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{date}/{apiVersion}/currencies/{endpoint}.json"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
