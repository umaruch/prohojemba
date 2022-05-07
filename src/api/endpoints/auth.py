from fastapi import APIRouter


router = APIRouter()


@router.post("/signin", tags=["Авторизация"])
async def signin():
    return "Hello, World"


@router.post("/token", tags=["Авторизация"])
async def token():
    pass


@router.post("/token/update", tags=["Авторизация"])
async def update_tokens_pair():
    pass


@router.post("/email/change", tags=["Авторизация"])
async def chenge_user_email():
    pass


@router.post("/password/change", tags=["Авторизация"])
async def change_user_password():
    pass


@router.post("/password/restore", tags=["Авторизация"])
async def restore_user_password():
    pass


@router.post("/email/validate", tags=["Авторизация"])
async def validate_email():
    pass