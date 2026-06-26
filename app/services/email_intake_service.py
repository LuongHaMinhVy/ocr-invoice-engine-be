import os

class EmailIntakeService:
    def __init__(self, upload_dir: str):
        self.upload_dir = upload_dir
        os.makedirs(self.upload_dir, exist_ok=True)

    def extract_attachments(self, msg) -> list:
        files = []
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            
            # Check content disposition or get filename directly
            filename = part.get_filename()
            if not filename:
                continue
                
            # Normalize extension and match against supported formats
            _, ext = os.path.splitext(filename.lower())
            if ext in ['.pdf', '.png', '.jpg', '.jpeg']:
                filepath = os.path.join(self.upload_dir, filename)
                payload = part.get_payload(decode=True)
                if payload:
                    with open(filepath, 'wb') as f:
                        f.write(payload)
                    files.append(filepath)
        return files
