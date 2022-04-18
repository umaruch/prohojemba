from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def get_titles_list():
    pass


@router.get("/{title_id}")
async def get_title(title_id: int):
    pass


@router.get("/{title_id}/activity")
async def get_title_activity(title_id: int):
    pass


@router.get("/{title_id}/reviews")
async def get_title_reviews(title_id: int):
    pass


@router.post("")
async def create_title():
    pass


@router.patch("/{title_id}")
async def edit_title(title_id: int):
    pass


@router.delete("/{title_id}")
async def delete_title(title_id: int):
    pass





