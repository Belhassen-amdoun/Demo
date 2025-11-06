# backend/main.py
import os
import tempfile
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from ocr import call_openai_ocr
from pdf_generator import generate_invoice_pdf

app = FastAPI(title="OCR Invoice Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Aucun fichier reçu")

    try:
        tmp_dir = tempfile.mkdtemp()
        tmp_path = os.path.join(tmp_dir, file.filename)
        with open(tmp_path, "wb") as f:
            f.write(await file.read())

        
        ocr_data = call_openai_ocr(tmp_path)

       
        pdf_path = os.path.join(tmp_dir, "invoice.pdf")
        generate_invoice_pdf(ocr_data, pdf_path)

        
        return JSONResponse({
            "ok": True,
            "paragraph": ocr_data.get("paragraph", ""),
            "pdf_url": f"/download?path={pdf_path}",
            "raw": ocr_data  
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download")
def download_file(path: str):
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Fichier introuvable")
    return FileResponse(path, media_type="application/pdf", filename="invoice.pdf")
