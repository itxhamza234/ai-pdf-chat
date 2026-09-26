import random
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
import os
from dotenv import load_dotenv

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)

def generate_otp() -> str:
    return str(random.randint(100000, 999999))

async def send_otp_email(email: EmailStr, otp: str):
    message = MessageSchema(
        subject="Your OTP Code",
        recipients=[email],
        body=f"Your OTP code is: {otp}. It will expire in 10 minutes.",
        subtype="plain",
    )
    fm = FastMail(conf)
    await fm.send_message(message)