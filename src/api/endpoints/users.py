from fastapi import APIRouter, Depends
from aioredis import Redis


from src.api.deps import get_repository, get_redis_connection
from src.repositories.users import UsersRepository


router = APIRouter()


@router.get("/@me")
async def get_current_user(
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)), 
    redis_cache: Redis = Depends(get_redis_connection)
):  
    await redis_cache.get("test")
    await users_repo.test()
    return {"status": "ok"}