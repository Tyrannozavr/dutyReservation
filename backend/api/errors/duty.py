from fastapi import HTTPException
from fastapi import status

UserHasNoPermission = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                    detail="The user doesn't have enough permissions")