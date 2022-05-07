from fastapi import APIRouter


router = APIRouter()


@router.post("", tags=["Активности"])
async def create_activity():
    pass


@router.patch("/{activity_id}", tags=["Активности"])
async def change_activity(activity_id: int):
    pass


@router.delete("/{activity_id}", tags=["Активности"])
async def delete_activity(activity_id: int):
    pass