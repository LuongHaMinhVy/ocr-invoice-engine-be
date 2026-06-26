import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_upload_invoice_success():
    # Attempt to upload a mock invoice file
    file_data = {"file": ("test_invoice.png", b"fake_image_bytes", "image/png")}
    response = client.post("/api/invoices/upload", files=file_data)
    assert response.status_code == 201
    json_data = response.json()
    assert json_data["vendor"] == "Extracted Vendor"
    assert json_data["total"] == 110.0
    assert "id" in json_data
