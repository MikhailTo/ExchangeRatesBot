from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: SecretStr
    exchange_rates_url_template: str = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{date}/{apiVersion}/currencies/{endpoint}.json"
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
