from email.message import EmailMessage
from aiosmtplib import send
import os


async def send_email(to: str, subject: str, body: str):
    message = EmailMessage()
    message["From"] = "noreply@example.com"
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body)

    await send(
        message,
        hostname=os.getenv("SMTP_HOST", "localhost"),
        port=os.getenv("SMTP_PORT", 1025),
    )
