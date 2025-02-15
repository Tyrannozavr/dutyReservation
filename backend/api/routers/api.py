from fastapi.requests import Request
from fastapi.routing import APIRouter

from . import auth, duty, room, users

router = APIRouter()

# @router.get("/test")
# async def get_request(request: Request):
#     print("params are: ", request.query_params)
#     print(">", request.headers, ">", request.path_params)
#     return "hello"

router.include_router(auth.router, tags=["auth"], prefix="/auth")
router.include_router(duty.router, tags=["duty"], prefix="/room")
router.include_router(duty.router_without_room, tags=["duty"], prefix="/duties")
router.include_router(duty.ws_router, tags=["duty"], prefix="/duties")

router.include_router(room.router, tags=["room"], prefix="/room")
router.include_router(users.router, tags=["users"], prefix="/users")
