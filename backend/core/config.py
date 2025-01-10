from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    telegram_bot_token: str = Field(alias='TELEGRAM_BOT_TOKEN')
    secret_key: str = Field(alias='SECRET_KEY')
    auth_algorithm: str = Field(alias='AUTH_ALGORITHM', default="HS256")
    access_token_expire_minutes: str = Field(alias='ACCESS_TOKEN_EXPIRE_MINUTES')
    refresh_token_expire_minutes: str = Field(alias='REFRESH_TOKEN_EXPIRE_MINUTES')

    class Config:
        env_file = ".env"

settings = Settings()

def get_settings() -> Settings:
    return settings