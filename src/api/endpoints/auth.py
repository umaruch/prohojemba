from fastapi import APIRouter


router = APIRouter()


@router.post("/signin")
async def signin():
    return "Hello, World"


@router.post("/token")
async def token():
    pass


@router.post("/token/update")
async def update_tokens_pair():
    pass


@router.post("/email/change")
async def chenge_user_email():
    pass


@router.post("/password/change")
async def change_user_password():
    pass


@router.post("/password/restore")
async def restore_user_password():
    pass


@router.post("/email/validate")
async def validate_email():
    pass