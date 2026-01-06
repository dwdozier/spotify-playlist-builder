import aiosmtplib
from email.message import EmailMessage
from backend.app.core.config import settings

from typing import Optional


async def send_email(to_email: str, subject: str, body: str, html_body: Optional[str] = None):
    message = EmailMessage()
    message["From"] = settings.EMAIL_FROM
    message["To"] = to_email
    message["Subject"] = subject
    message.set_content(body)

    if html_body:
        message.add_alternative(html_body, subtype="html")

    await aiosmtplib.send(
        message,
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        username=settings.SMTP_USER,
        password=settings.SMTP_PASSWORD,
        use_tls=False if settings.SMTP_PORT == 1025 else True,
    )
