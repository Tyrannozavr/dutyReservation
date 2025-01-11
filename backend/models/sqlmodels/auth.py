from typing import Optional, Any

from sqlmodel import SQLModel, Field, Relationship

from models.pydantic.auth import UserOriginsTypes

TELEGRAM_PREFIX = "tg_999_"



def generate_user_link(username: str, origin: UserOriginsTypes):
    if origin is UserOriginsTypes.telegram:
        return f"https://t.me/{username}"

class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    first_name: str | None = Field(default=None)
    last_name: str | None = Field(default=None)
    internal_username: str = Field(unique=True)
    tg_data: Optional["TelegramUserData"] = Relationship(back_populates="user")
    duties: Optional["Duty"] = Relationship(back_populates="user")

    @property
    def username(self):
        if self.is_from_telegram:
            return self.internal_username[len(TELEGRAM_PREFIX):]
        return self.internal_username


    @property
    def link(self):
        if self.is_from_telegram:
            return generate_user_link(username=self.username, origin=UserOriginsTypes.telegram)
        return ""


    @property
    def is_from_telegram(self):
        return self.internal_username.startswith(TELEGRAM_PREFIX)

    def model_dump(self, *args, **kwargs):
        # Call the original model_dump method to get all fields
        data = super().model_dump(*args, **kwargs)

        # Replace 'internal_username' with 'username'
        data['username'] = self.username

        # Optionally remove 'internal_username' if you don't want it in the output
        data.pop('internal_username', None)

        return data


    def __init__(self, **data: Any):
        if "username" in data:
            self.internal_username = data.get("username")
        super().__init__(**data)


class TelegramUserData(SQLModel, table=True):
    telegram_id: int = Field(primary_key=True)
    language_code: str | None = Field(default=None)
    allows_write_to_pm: bool | None = Field(default=None)
    photo_url: str | None = Field(default=None)

    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="tg_data")



    def __int__(self, **data):
        user_data = {}
        if "first_name" in data:
            user_data["first_name"] = data.pop("first_name")
        if "last_name" in data:
            user_data["last_name"] = data.pop("last_name")
        if "username" in data:
            user_data["username"] = data.pop("username")

        # Initialize the User model if user_data is populated
        if user_data:
            self.user = User(**user_data)
        super().__init__(**data)

    class Config:
        from_attributes = True

#
# 'user=%7B%22id%22%3A972834722%2C%22first_name%22%3A%22%D0%94%D0%BC%D0%B8%D1%82%D1%80%D0%B8%D0%B9%22%2C%22last_name%22%3A%22%D0%A1%D1%87%D0%B8%D1%81%D0%BB%D1%91%D0%BD%D0%BE%D0%BA%22%2C%22username%22%3A%22tyrannozavr%22%2C%22language_code%22%3A%22ru%22%2C%22allows_write_to_pm%22%3Atrue%2C%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2FxJjYkAlqp7Mvl8tGiKvIH2Qvh2SEY2ZYE2gKivsD9qU.svg%22%7D&chat_instance=5919894213088809580&chat_type=private&auth_date=1736280453&signature=ru-H3ccFkx-Z1bBwBQ98MW38-3C02T2cAUbf0yP94VbJEKp0kcWI2VWVs_4U4vJm2_Zilxj6BDIFTH54uI8jBA&hash=93063c75042cb6076876c9d7b4540e409c6e71338454e9dcb93dfeb1'
#
# {
#   "user": {
#     "id": 972834722,
#     "first_name": "Дмитрий",
#     "last_name": "Счислёнок",
#     "username": "tyrannozavr",
#     "language_code": "ru",
#     "allows_write_to_pm": true,
#     "photo_url": "https://t.me/i/userpic/320/xJjYkAlqp7Mvl8tGiKvIH2Qvh2SEY2ZYE2gKivsD9qU.svg"
#   },
#   "chat_instance": 5919894213088809580,
#   "chat_type": "private",
#   "auth_date": 1736280453,
#   "signature": "ru-H3ccFkx-Z1bBwBQ98MW38-3C02T2cAUbf0yP94VbJEKp0kcWI2VWVs_4U4vJm2_Zilxj6BDIFTH54uI8jBA",
#   "hash": "93063c75042cb6076876c9d7b4540e409c6e71338454e9dcb93dfeb1"
# }



# class TelegramUser(SQLModel):
#     id: int = Field(primary_key=True)
#     first_name: str = Field()
#     last_name: str | None = Field(default=None)
#     username: str | None = Field(default=None)
#     language_code: str | None = Field(default=None)
#     allows_write_to_pm: bool | None = Field(default=None)
#     photo_url: str | None = Field(default=None)
#
# class TelegramInitDataModel(SQLModel):
#     user_id: int = Field(foreign_key="telegramuser.id")
#     chat_instance: int = Field()
#     chat_type: str = Field()
#     auth_date: int = Field()
#     signature: str = Field()
#     hash: str = Field()
