from fastapi import APIRouter

router = APIRouter()


@router.post("")
async def create_activity():
    pass


@router.patch("/{activity_id}")
async def edit_activity(activity_id: int):
    pass


@router.delete("/{activity_id}")
async def delete_activity(activity_id: int):
    pass