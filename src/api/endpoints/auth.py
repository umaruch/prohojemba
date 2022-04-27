from fastapi import APIRouter


router = APIRouter()


@router.post("/signin")
async def signin():
    return "Hello, World"


@router.post("/token")
async def token():
    pass
