import os
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.invoice import Invoice
from app.models.invoice_item import InvoiceItem
from app.models.invoice_status import InvoiceStatus

router = APIRouter(prefix="/api/invoices", tags=["invoices"])

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/health")
def health_check():
    return {"status": "OK"}

@router.post("/upload", status_code=201)
async def upload_invoice(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if file.content_type not in ["image/png", "image/jpeg", "application/pdf"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Simulated Gemini extraction & math validation
    vendor = "Extracted Vendor"
    subtotal, vat, total = 100.0, 10.0, 110.0
    status_val = InvoiceStatus.VALIDATED
    
    invoice = Invoice(
        vendor=vendor,
        subtotal=subtotal,
        vat=vat,
        total=total,
        file_path=file_path,
        status=status_val
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    
    item = InvoiceItem(
        invoice_id=invoice.id,
        name="Extracted Item",
        quantity=1.0,
        unit_price=100.0,
        total=100.0
    )
    db.add(item)
    db.commit()
    
    return {
        "id": invoice.id,
        "vendor": invoice.vendor,
        "total": invoice.total,
        "status": invoice.status.value
    }

