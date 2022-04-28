from fastapi import APIRouter, Form


from src.services import email


router = APIRouter()


@router.post("/email")
async def test_send_mail(client_email: str = Form(...)):
    await email.send_email(client_email)
    return {"status": "ok"}