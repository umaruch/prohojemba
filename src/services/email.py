from email.message import EmailMessage
import aiosmtplib


from src.core.settings import settings


async def send_email(client_email: str) -> None:
    message = EmailMessage()
    message["From"] = settings.mail.SENDER
    message["To"] = client_email
    message["Subject"] = "Test message"
    message.set_content("Здраствуйте, я беcполезный вирус, потому просто проигнорируйте это письмо.") 
 
    await aiosmtplib.send(
        message=message,
        **settings.mail.kwargs
    )