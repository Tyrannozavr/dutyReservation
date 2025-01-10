from pydantic import BaseModel


class TelegramUserDataInDb(BaseModel):
    id: int
    first_name: str
    last_name: str | None
    username: str | None
    language_code: str | None
    allows_write_to_pm: bool | None
    photo_url: str | None


class TelegramInitData(BaseModel):
    user: TelegramUserDataInDb
    chat_instance: int
    chat_type: str | None


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str