# backend/pdf_generator.py
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

def generate_invoice_pdf(data: dict, output_path: str):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    y = height - 40 * mm

    c.setFont("Helvetica-Bold", 16)
    c.drawString(30 * mm, y, "FACTURE")
    y -= 15 * mm

    c.setFont("Helvetica", 12)
    c.drawString(30 * mm, y, f"Client : {data.get('client', '')}")
    y -= 8 * mm
    c.drawString(30 * mm, y, f"Date : {data.get('date', '')}")
    y -= 8 * mm
    c.drawString(30 * mm, y, f"Montant : {data.get('montant', '')} {data.get('currency', '')}")
    y -= 12 * mm
    c.drawString(30 * mm, y, "Description :")
    y -= 8 * mm

    desc = data.get("description", "")
    text = c.beginText(30 * mm, y)
    text.setLeading(14)
    for line in desc.splitlines():
        text.textLine(line)
    c.drawText(text)

    c.setFont("Helvetica-Oblique", 10)
    
    c.save()
