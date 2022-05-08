from fastapi import APIRouter, Depends
from aioredis import Redis


from src.api import deps
from src.repositories.users import UsersRepository


router = APIRouter()


@router.get("/@me", tags=["Пользователи"])
async def get_current_user(
    user_id: int = Depends(deps.get_current_user_by_access_token)
):  
    return user_id


@router.patch("/@me", tags=["Пользователи"])
async def change_current_user_profile():
    pass


@router.get("/@me/reviews", tags=["Пользователи"])
async def get_current_user_reviews():
    pass


@router.get("/@me/activity", tags=["Пользователи"])
async def get_current_user_activity():
    pass


@router.get("/{user_id}", tags=["Пользователи"])
async def get_user_profile(user_id: int):
    pass


@router.get("/{user_id}/reviews", tags=["Пользователи"])
async def get_user_reviews(user_id: int):
    pass


@router.get("/{user_id}/activity", tags=["Пользователи"])
async def get_user_activity(user_id: int):
    pass

