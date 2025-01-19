from datetime import datetime, timezone, timedelta

import jwt
from jwt import InvalidTokenError
from passlib.context import CryptContext
from sqlmodel import Session

from api.errors.auth import IncorrectUsernameOrPassword, UserAlreadyExist, TokenHasExpired, InvalidToken
from db.repositories.auth import UserRepositories
from models.pydantic.auth import Token, TokenData, UserDbCreate, UserOriginTypes, UserDataCreate, TelegramUserDataIn
from models.sqlmodels.auth import User, TelegramUserData


class TokenServices:
    def __init__(self, secret_key: str, algorithm: str, access_expire_time: float = 60,
                 refresh_expire_time: float = 20160, token_type: str = "bearer"):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_token_expire_minutes = access_expire_time
        self.refresh_token_expire_minutes = refresh_expire_time
        self.token_type = token_type

    async def _create_token(self, data: TokenData, expire_time: float):
        if expire_time <= 0:
            raise Exception("expire time must be grater than zero")
        expires_delta = timedelta(minutes=expire_time)
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.exp = expire
        encoded_jwt = jwt.encode(to_encode.model_dump(), self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    async def _create_access_token(self, data: TokenData):
        expire_time = float(self.access_token_expire_minutes)
        access_token = await self._create_token(data=data, expire_time=expire_time)
        return access_token

    async def _create_refresh_token(self, data: TokenData):
        expire_time = float(self.refresh_token_expire_minutes)
        data.type = "refresh"
        refresh_token = await self._create_token(data=data, expire_time=expire_time)
        return refresh_token

    async def get_tokens(self, data: TokenData):
        access_token = await self._create_access_token(data=data)
        refresh_token = await self._create_refresh_token(data=data)
        return Token(access_token=access_token, refresh_token=refresh_token, token_type=self.token_type)

    async def decode_token(self, token: str) -> TokenData:
        try:
            data = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            # Check if the token is expired
            if 'exp' in data and datetime.fromtimestamp(data['exp'], timezone.utc) < datetime.now(timezone.utc):
                print("is expired")
                raise TokenHasExpired
            return TokenData(**data)
        except jwt.ExpiredSignatureError:
            raise TokenHasExpired
        except jwt.InvalidTokenError:
            raise InvalidToken


class UserServices:
    def __init__(self, db: Session, pwd_context: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto"),
                 repositories: "UserRepositories" = None):
        self.db = db
        self.pwd_context = pwd_context
        self.repositories = UserRepositories(db=db) if not repositories else repositories

    async def _get_hashed_password(self, plaintext_password: str) -> str:
        if plaintext_password is None:
            raise ValueError("The password can not be None")
        return self.pwd_context.hash(plaintext_password)

    async def verify_password(self, plaintext_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plaintext_password, hashed_password)

    async def authenticate_user(self, username: str, password: str):
        user = await self.repositories.get_user_by_username(username=username)
        if not user:
            raise IncorrectUsernameOrPassword
        if not await self.verify_password(plaintext_password=password, hashed_password=user.hashed_password):
            raise IncorrectUsernameOrPassword
        return user

    async def is_username_already_taken(self, username: str) -> bool:
        return await self.repositories.is_username_already_taken(username=username)

    async def validate_if_username_is_already_taken(self, username: str):
        user = await self.is_username_already_taken(username=username)
        if user:
            raise UserAlreadyExist

    async def get_or_create_tg_user(self, init_data: TelegramUserDataIn) -> TelegramUserData:
        tg_user = await self.repositories.get_tg_user_by_id(init_data.id)
        if tg_user:
            return tg_user
        username = init_data.username
        if await self.repositories.is_username_already_taken(username):
            username = None
        user_data = UserDataCreate(
            username=username,
            first_name=init_data.first_name,
            last_name=init_data.last_name,
        )
        user = await self.create_user(origin=UserOriginTypes.telegram, user_data=user_data)
        tg_data = await self.repositories.create_tg_user(init_data=init_data)
        tg_data.user = user
        self.db.commit()
        self.db.refresh(tg_data)
        return tg_data

    async def create_user(self, user_data: UserDataCreate, origin: UserOriginTypes) -> User:
        await self.validate_if_username_is_already_taken(username=user_data.username)
        user_db = UserDbCreate(**user_data.model_dump(),
                               hashed_password=await self._get_hashed_password(
                                   user_data.password) if user_data.password else None,
                               origin=origin)
        user = await self.repositories.create_user(user_data=user_db)
        self.db.commit()
        self.db.refresh(user)
        return user

    async def get_all_users(self):
        return await self.repositories.get_all_users()

    async def get_user_by_username(self, username):
        return await self.repositories.get_user_by_username(username)

    async def get_user_by_id(self, user_id: int):
        return await self.repositories.get_user_by_id(user_id=user_id)
