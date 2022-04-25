from fastapi import APIRouter

router = APIRouter()


@router.post("")
async def create_review():
    pass


@router.patch("/{review_id}")
async def edit_review(review_id: int):
    pass


@router.delete("/{review_id}")
async def delete_review(review_id: int):
    pass