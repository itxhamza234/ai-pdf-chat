from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import SessionLocal
from core.security import get_current_user_id
from models.user import User
from schemas.user import UserUpdate

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/me")
def get_profile(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "is_verified": user.is_verified,
        "created_at": user.created_at,
    }


@router.put("/me")
def update_profile(
    data: UserUpdate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if data.name is not None:
        user.name = data.name

    if data.email is not None:
        existing = db.query(User).filter(User.email == data.email).first()
        if existing and existing.id != user.id:
            raise HTTPException(status_code=400, detail="Email already in use")
        user.email = data.email

    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "is_verified": user.is_verified,
    }