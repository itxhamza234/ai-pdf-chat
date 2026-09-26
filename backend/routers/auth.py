from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from core.database import SessionLocal
from schemas.user import UserSignup, OTPVerify
from models.user import User
from models.otp import OTP
from core.security import hash_password
from core.email import generate_otp, send_otp_email

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup")
async def signup(user_data: UserSignup, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    otp_code = generate_otp()
    new_otp = OTP(
        user_id=new_user.id,
        code=otp_code,
        purpose="email_verification",
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),
    )
    db.add(new_otp)
    db.commit()

    await send_otp_email(new_user.email, otp_code)

    return {"message": "User created. OTP sent to email.", "user_id": new_user.id}


@router.post("/verify-email")
def verify_email(data: OTPVerify, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.is_verified:
        return {"message": "Email already verified"}

    otp_record = (
        db.query(OTP)
        .filter(
            OTP.user_id == user.id,
            OTP.code == data.otp,
            OTP.purpose == "email_verification",
            OTP.is_used == False,
        )
        .order_by(OTP.created_at.desc())
        .first()
    )

    if not otp_record:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if otp_record.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="OTP expired")

    user.is_verified = True
    otp_record.is_used = True
    db.commit()

    return {"message": "Email verified successfully"}