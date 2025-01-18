from enum import Enum


class UserOriginTypes(str, Enum):
    telegram = "telegram"
    web = "web"
