from fastapi import APIRouter

router = APIRouter()


@router.get("/{user_id}")
async def get_user_profile(user_id: int|str):
    pass


@router.get("/{user_id}/activity")
async def get_user_walks(user_id: int|str):
    pass


@router.get("/{user_id}/reviews")
async def get_user_walks(user_id: int|str):
    pass


@router.patch("/@me")
async def edit_current_user_profile():
    pass