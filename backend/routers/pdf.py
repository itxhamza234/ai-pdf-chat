import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pypdf import PdfReader

from core.database import SessionLocal
from core.security import get_current_user_id
from core.chunking import chunk_text
from core.embeddings import generate_embedding
from models.pdf import PDFDocument
from models.chunk import PDFChunk

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


UPLOAD_DIR = "uploads"
@router.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...),
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    user_folder = os.path.join(UPLOAD_DIR, str(user_id))
    os.makedirs(user_folder, exist_ok=True)
    file_path = os.path.join(user_folder, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    reader = PdfReader(file_path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() or ""

    if not full_text.strip():
        raise HTTPException(status_code=400, detail="Could not extract any text from this PDF")

    new_pdf = PDFDocument(
        user_id=user_id,
        filename=file.filename,
        file_path=file_path,
    )
    db.add(new_pdf)
    db.commit()
    db.refresh(new_pdf)

    chunks = chunk_text(full_text)

    for chunk in chunks:
        embedding = generate_embedding(chunk)
        new_chunk = PDFChunk(
            pdf_id=new_pdf.id,
            user_id=user_id,
            content=chunk,
            embedding=embedding,
        )
        db.add(new_chunk)

    db.commit()

    return {
        "message": "PDF uploaded and processed successfully",
        "pdf_id": new_pdf.id,
        "chunks_created": len(chunks),
    }

@router.get("/list")
def list_pdfs(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    pdfs = db.query(PDFDocument).filter(PDFDocument.user_id == user_id).all()
    return [{"id" : pdf.id, "filename":pdf.filename, "uploaded_at": pdf.uploaded_at}for pdf in pdfs]


@router.delete("/{pdf_id}")
def delete_pdf(pdf_id: int, user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db) ):
    pdf = db.query(PDFDocument).filter(PDFDocument.id == pdf_id, PDFDocument.user_id == user_id).first()
    if not pdf:
        raise HTTPException(status_code=404, detail="PDF not found")

    db.query(PDFChunk).filter(PDFChunk.pdf_id == pdf_id).delete()

    if os.path.exists(pdf.file_path):
        os.remove(pdf.file_path)

    db.delete(pdf)
    db.commit()

    return {"message": "PDF deleted successfully"}