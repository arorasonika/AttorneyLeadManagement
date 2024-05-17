from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("ATTORNEY_EMAIL_ID"),
    MAIL_PASSWORD=os.getenv("ATTORNEY_EMAIL_APP_PASSWORD"),
    MAIL_FROM=os.getenv("ATTORNEY_EMAIL_ID"),
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)

async def send_email(to_email: EmailStr, subject: str, body: str):
    message = MessageSchema(
        subject=subject,
        recipients=[to_email],
        body=body,
        subtype=MessageType.html
    )
    fm = FastMail(conf)
    await fm.send_message(message)
    
