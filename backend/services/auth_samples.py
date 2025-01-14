from passlib.context import CryptContext

from core.config import get_settings
from services.auth import UserServices, TokenServices

settings = get_settings()

user_services = UserServices(pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto"))
token_services = TokenServices(secret_key=settings.secret_key, algorithm=settings.auth_algorithm,
                               access_expire_time=float(settings.access_token_expire_minutes),
                               refresh_expire_time=float(settings.refresh_token_expire_minutes),
                               token_type="bearer")
