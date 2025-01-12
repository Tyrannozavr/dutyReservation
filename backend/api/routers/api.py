from fastapi.routing import APIRouter
from . import auth, duty

router = APIRouter()

router.include_router(auth.router, tags=["auth"], prefix="/auth")
router.include_router(duty.router, tags=["duty"], prefix="/duty")