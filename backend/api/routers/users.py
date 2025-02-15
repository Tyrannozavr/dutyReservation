from fastapi import APIRouter

from api.dependencies.auth import user_services_dep
from api.dependencies.users import username_dep

router = APIRouter()


@router.get("check-username")
async def check_username(
        username: username_dep,
        user_services: user_services_dep
) -> bool:
    return await user_services.is_username_already_taken(username=username)