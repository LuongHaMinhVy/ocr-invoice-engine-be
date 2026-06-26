import pytest
from unittest.mock import patch
from app.services.hermes_service import HermesService

@patch("requests.post")
def test_send_notification(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"status": "success"}

    service = HermesService(bridge_url="http://localhost:8089", target="telegram:-1002148765432")
    success = service.send_invoice_notification(invoice_id=1, vendor="Cửa hàng tiện lợi", total=50000.0, status="VALIDATED")
    
    assert success is True
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert kwargs["json"]["target"] == "telegram:-1002148765432"
    assert "Cửa hàng tiện lợi" in kwargs["json"]["message"]
