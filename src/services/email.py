from email.message import EmailMessage
import aiosmtplib


from src.core.settings import settings


async def _send_email(client_email: str, text_email: str) -> None:
    message = EmailMessage()
    message["From"] = settings.mail.SENDER
    message["To"] = client_email
    message["Subject"] = "Test message"
    message.set_content(text_email) 
 
    await aiosmtplib.send(
        message=message,
        **settings.mail.kwargs
    )


async def send_register_message(email: str, code: str) -> None:
    text = f"Регистрация. Ваш код проверки email: {code}"
    await _send_email(email, text)