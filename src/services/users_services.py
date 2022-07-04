from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from fastapi.exceptions import HTTPException

from src.crud import users_crud
from src.schemes import users_schemes
from src.services import image_services
from src.models.users import User


async def get_user_info(db: AsyncSession, user_id: int) -> User:
    user = await users_crud.get_by_id(db, user_id)
    if user:
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )


async def update_user_info(db: AsyncSession, user_id: int, form: users_schemes.PatchUserForm) -> None:
    update_data = {}
    for key, value in form.fields().items():
        if value:
            update_data[key] = value

    # Сохранение изображения
    if form.avatar:
        update_data["avatar_uri"] = image_services.save_image(form.avatar)

    if update_data:
        await users_crud.update(db, user_id, **update_data)