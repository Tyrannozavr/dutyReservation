from fastapi import HTTPException
from fastapi import status


# UserHasNoPermission = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                                     detail="The user doesn't have enough permissions")
class UserHasNoPermission(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="The user doesn't have enough permissions")
