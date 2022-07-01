import aiosmtplib

async def _send_email() -> None:
    pass


async def send_validation_email(email: str, code: str) -> None:
    print(f"Код валидации для {email}: {code}")