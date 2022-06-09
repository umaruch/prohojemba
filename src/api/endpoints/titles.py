from fastapi import APIRouter


router = APIRouter()


@router.get("", tags=["Тайтлы"])
async def get_titles(type: str, offset: int, limit: int) -> None:
    pass


@router.post("", tags=["Тайтлы"])
async def create_title():
    pass


@router.get("/{title_id}", tags=["Тайтлы"])
async def get_title(title_id: int):
    pass


@router.patch("/{title_id}", tags=["Тайтлы"])
async def change_title(title_id: int):
    pass


@router.delete("/{title_id}", tags=["Тайтлы"])
async def delete_title(title_id: int):
    pass


@router.get("/{title_id}/reviews", tags=["Тайтлы"])
async def get_title_reviews(title_id: int):
    pass


@router.get("/{title_id}/activity", tags=["Тайтлы"])
async def get_title_activity(title_id: int):
    pass