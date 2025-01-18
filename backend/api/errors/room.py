from fastapi import HTTPException, status

RoomNotFound = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Room not found")
InvalidRoomData = HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid room data")
