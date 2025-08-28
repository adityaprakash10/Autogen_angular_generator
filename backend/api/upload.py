from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import io

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        filename = file.filename.lower()
        
        if filename.endswith(".pdf"):
            import pdfplumber
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                pages = [page.extract_text() for page in pdf.pages if page.extract_text()]
            raw_text = "\n".join(pages)

        elif filename.endswith(".docx"):
            from docx import Document
            doc = Document(io.BytesIO(content))
            paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
            raw_text = "\n".join(paragraphs)

        elif filename.endswith(".md") or filename.endswith(".txt"):
            raw_text = content.decode("utf-8", errors="ignore")

        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Upload PDF, DOCX, or MD files.")

        return JSONResponse({"raw_text": raw_text})

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to process file: {e}")
