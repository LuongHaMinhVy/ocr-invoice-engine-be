import os
import pytest
from unittest.mock import MagicMock
from email.message import EmailMessage
from app.services.email_intake_service import EmailIntakeService

@pytest.fixture
def mock_upload_dir(tmp_path):
    d = tmp_path / "uploads"
    d.mkdir()
    return str(d)

def test_extract_attachments(mock_upload_dir):
    # Create a mock EmailMessage with an attachment
    msg = EmailMessage()
    msg['Subject'] = "Invoice test"
    msg['From'] = "vendor@example.com"
    msg['To'] = "user@example.com"
    msg.set_content("Here is your invoice.")
    
    # Add attachment
    file_content = b"pdf_data_bytes"
    msg.add_attachment(file_content, maintype="application", subtype="pdf", filename="invoice.pdf")
    
    service = EmailIntakeService(upload_dir=mock_upload_dir)
    extracted_files = service.extract_attachments(msg)
    
    assert len(extracted_files) == 1
    assert os.path.exists(extracted_files[0])
    assert os.path.basename(extracted_files[0]) == "invoice.pdf"
    with open(extracted_files[0], "rb") as f:
        assert f.read() == file_content
