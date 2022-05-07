from fastapi import APIRouter, Depends
from aioredis import Redis


from src.api.deps import get_repository, get_redis_connection
from src.repositories.users import UsersRepository


router = APIRouter()


@router.get("/@me", tags=["Пользователи"])
async def get_current_user(
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)), 
    redis_cache: Redis = Depends(get_redis_connection)
):  
    await redis_cache.get("test")
    await users_repo.test()
    return {"status": "ok"}


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

