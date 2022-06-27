from fastapi import APIRouter, Form




router = APIRouter()


@router.patch("/{activity_id}", tags=["Активность"])
async def change_activity(activity_id: int,
    state: str = Form(...)
):
    """
        Редактирование активности
    """
    pass


@router.delete("/{activity_id}", tags=["Активность"])
async def delete_activity(activity_id: int):
    """
        Удаление активности
    """
    pass