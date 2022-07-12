from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api import deps
from src.services import users_services
from src.schemes import users_schemes


router = APIRouter()


@router.get("/@me", tags=["Пользователи"])
async def get_current_user(
    current_user_id: int = Depends(deps.get_current_user_id),
    db: AsyncSession = Depends(deps.get_db_session)
) -> users_schemes.CurrentUserOutput:  
    user = await users_services.get_user_info(db, current_user_id)
    return users_schemes.CurrentUserOutput.from_orm(user)


@router.patch("/@me", tags=["Пользователи"])
async def change_current_user_profile(
    current_user_id: int = Depends(deps.get_current_user_id),
    form: users_schemes.PatchUserForm = Depends(users_schemes.PatchUserForm),
    db: AsyncSession = Depends(deps.get_db_session)
):
    await users_services.update_user_info(db, current_user_id, form)


@router.get("/{user_id}", tags=["Пользователи"])
async def get_user_profile(
    user_id: int,
    current_user_id: int = Depends(deps.get_current_user_id),
    db: AsyncSession = Depends(deps.get_db_session)
) -> users_schemes.UserOutput:
    user = await users_services.get_user_info(db, user_id)
    return users_schemes.UserOutput.from_orm(user)


@router.get("/@me/activities", tags=["Активность"])
async def get_current_user_activities(
    current_user_id: int = Depends(deps.get_current_user_id),
    limit: int = 20,
    offset: int = 0
):
    pass


@router.get("/{user_id}/activities", tags=["Активность"])
async def get_user_activity(
    user_id: int,
    current_user_id: int = Depends(deps.get_current_user_id),
    limit: int = 20,
    offset: int = 0
):
    """
        Получение списка активностей пользователя    
    """
    pass

