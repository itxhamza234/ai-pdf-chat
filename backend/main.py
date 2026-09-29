from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.database import engine, Base
from sqlalchemy import text
from models.user import User
from models.otp import OTP
from routers.auth import router as auth_router
from routers.user import router as user_router
from models.pdf import PDFDocument
from models.chunk import PDFChunk
from routers.pdf import router as pdf_router
from routers.chat import router as chat_router
from models.chat import ChatMessage

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(user_router, prefix="/user", tags=["User"])
app.include_router(pdf_router, prefix="/pdf", tags=["PDF"])
app.include_router(chat_router, prefix="/chat", tags=["Chat"])

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/db-check")
def db_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return {"database": "connected"}