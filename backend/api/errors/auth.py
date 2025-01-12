from fastapi import HTTPException

IncorrectUsernameOrPassword = HTTPException(status_code=401, detail="Incorrect username or password")