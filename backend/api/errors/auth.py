from fastapi import HTTPException, status

IncorrectUsernameOrPassword = HTTPException(status_code=401, detail="Incorrect username or password")


class TelegramInitDataIncorrect(HTTPException):
    """Inherited from class to have ability catch this exception with try except statement"""

    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Telegram init data incorrect")


class UserAlreadyExist(HTTPException):
    """Inherited from class to have ability catch this exception with try except statement"""

    def __init__(self):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail="User already exist")

TokenHasExpired = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The token has expired")
InvalidToken = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The token is invalid")