from fastapi import APIRouter, Depends


from src.api import deps
from src.models.users import User
from src.schemes.users import CurrentUserProfile


router = APIRouter()


@router.get("/@me", tags=["Пользователи"], response_model=CurrentUserProfile)
async def get_current_user(
    user: User = Depends(deps.get_current_user_by_access_token)
):   
    return user


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

