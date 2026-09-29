import re
from core.mcp_client import call_word_definition
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from google import genai
import os

from core.database import SessionLocal
from core.security import get_current_user_id
from core.embeddings import generate_embedding
from models.pdf import PDFDocument
from models.chunk import PDFChunk
from models.chat import ChatMessage

router = APIRouter()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ChatRequest(BaseModel):
    pdf_id: int
    question: str

@router.post("/ask")
async def ask(data: ChatRequest, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    pdf = db.query(PDFDocument).filter(PDFDocument.id == data.pdf_id, PDFDocument.user_id == user_id).first()
    if not pdf:
        raise HTTPException(status_code=404, detail="PDF not found")

    match = re.search(r"(?:meaning of|define|what does)\s+([a-zA-Z]+)", data.question, re.IGNORECASE)
    if match:
        word = match.group(1)
        definition = await call_word_definition(word)
        answer = f"{word}: {definition}"
        db.add(ChatMessage(pdf_id=data.pdf_id, user_id=user_id, question=data.question, answer=answer))
        db.commit()
        return {"answer": answer}

    q_embedding = generate_embedding(data.question)

    chunks = (
        db.query(PDFChunk)
        .filter(PDFChunk.pdf_id == data.pdf_id)
        .order_by(PDFChunk.embedding.cosine_distance(q_embedding))
        .limit(4)
        .all()
    )
    context = "\n\n".join(c.content for c in chunks)

    prompt = f"""Answer the question using only the context below. If the answer isn't in the context, say exactly: "I could not find this information in the selected document."

Context:
{context}

Question: {data.question}"""

    try:
        response = client.models.generate_content(model="gemini-3.8-flash", contents=prompt)
        answer = response.text
    except Exception:
        raise HTTPException(status_code=503, detail="AI service is temporarily busy. Please try again in a moment.")

    db.add(ChatMessage(pdf_id=data.pdf_id, user_id=user_id, question=data.question, answer=answer))
    db.commit()

    return {"answer": answer}

@router.get("/history/{pdf_id}")
def get_history(pdf_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    messages = (
        db.query(ChatMessage)
        .filter(ChatMessage.pdf_id == pdf_id, ChatMessage.user_id == user_id)
        .order_by(ChatMessage.created_at)
        .all()
    )
    return [{"question": m.question, "answer": m.answer, "created_at": m.created_at} for m in messages]