from fastapi import Body
from pydantic import BaseModel, Field

class TelegramUserDataInDb(BaseModel):
    id: int
    first_name: str
    last_name: str | None
    username: str | None
    language_code: str | None
    allows_write_to_pm: bool | None
    photo_url: str | None


class TelegramInitDataInDb(BaseModel):
    user: TelegramUserDataInDb
    chat_instance: int
    chat_type: str | None
