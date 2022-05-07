from fastapi import APIRouter


router = APIRouter()


@router.post("", tags=["Отзывы"])
async def create_review():
    pass


@router.patch("/{review_id}", tags=["Отзывы"])
async def change_review(review_id: int):
    pass


@router.delete("/{review_id}", tags=["Отзывы"])
async def delete_review(review_id: int):
    pass