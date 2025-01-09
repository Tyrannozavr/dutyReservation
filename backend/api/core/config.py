from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    telegram_bot_token: str = Field(alias='TELEGRAM_BOT_TOKEN')

    class Config:
        env_file = ".env"

settings = Settings()

def get_settings() -> Settings:
    return settings