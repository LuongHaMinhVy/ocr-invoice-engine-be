import requests
import logging

logger = logging.getLogger(__name__)

class HermesService:
    def __init__(self, bridge_url: str, target: str):
        self.bridge_url = bridge_url
        self.target = target

    def send_invoice_notification(self, invoice_id: int, vendor: str, total: float, status: str) -> bool:
        if not self.bridge_url or not self.target:
            logger.warning("Hermes configuration missing. Skipping notification.")
            return False

        message = (
            f"🔔 [OCR Invoice] Phát hiện hóa đơn mới!\n"
            f"- Nhà cung cấp: {vendor}\n"
            f"- Tổng tiền: {total:,.2f} VNĐ\n"
            f"- Trạng thái xác thực: {status}\n"
            f"- Link đối chiếu: http://localhost:3000/invoices/{invoice_id}"
        )

        try:
            response = requests.post(
                f"{self.bridge_url}/api/notifications",
                json={"target": self.target, "message": message},
                timeout=5
            )
            if response.status_code == 200:
                logger.info("Notification successfully sent to Hermes.")
                return True
            else:
                logger.error(f"Hermes bridge returned status {response.status_code}: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Failed to send notification to Hermes: {e}")
            return False
