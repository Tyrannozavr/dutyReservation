from fastapi.routing import APIRouter

from . import auth, duty, room

router = APIRouter()

router.include_router(auth.router, tags=["auth"], prefix="/auth")
router.include_router(duty.router, tags=["duty"], prefix="/duty")
router.include_router(room.router, tags=["room"], prefix="/room")
