from fastapi import APIRouter

router = APIRouter()


@router.post("/signin")
async def sign_in():
    pass


@router.get("/signin/validate")
async def sign_in_validate_email():
    pass


@router.post("/token")
async def login():
    pass


@router.post("/token/update")
async def update_tokens_pair():
    pass


@router.post("/email/change")
async def update_user_email():
    pass


@router.get("/email/change/validate")
async def update_user_email_validate_email():
    pass


@router.post("/password/change")
async def update_user_password():
    pass


@router.post("/password/restore")
async def restore_user_password():
    pass


@router.get("/password/restore/validate")
async def restore_user_password_validate_email():
    pass