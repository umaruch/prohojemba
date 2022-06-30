from typing import Optional
from fastapi import APIRouter, Depends, Form, File, UploadFile


from src.api import deps


router = APIRouter()


@router.get("/@me", tags=["Пользователи"])
async def get_current_user(
    current_user: int = Depends(deps.get_current_user_id)
):   
    pass


@router.patch("/@me", tags=["Пользователи"])
async def change_current_user_profile(
    username: Optional[str] = Form(None),
    avatar: Optional[UploadFile] = File(None)
):
    pass


@router.get("/{user_id}", tags=["Пользователи"])
async def get_user_profile(
    user_id: int
):
    pass


@router.get("/@me/activities", tags=["Активность"])
async def get_current_user_activities(
    limit: int,
    offset: int
):
    pass


@router.get("/{user_id}/activities", tags=["Активность"])
async def get_user_activity(
    user_id: int,
    limit: int,
    offset: int
):
    """
        Получение списка активностей пользователя    
    """
    pass

