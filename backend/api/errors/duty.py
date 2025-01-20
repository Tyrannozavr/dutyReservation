from fastapi import HTTPException
from fastapi import status


# UserHasNoPermission = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                                     detail="The user doesn't have enough permissions")
class UserHasNoPermission(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="The user doesn't have enough permissions")

class DutyIsAlreadyTaken(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="The date is already taken or there is no such"
                                                                       " a duty in this room")

class UserAlreadyTookAllDuties(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="The user already have took all duties")

DutyDoesntExist = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The duty doesn't exist")
DutyDoesntMatchRoom = HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="The duty doesn't exist in this room")