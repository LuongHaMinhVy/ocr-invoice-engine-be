import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    TESTING: bool = os.getenv("TESTING", "false").lower() == "true"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///test.db" if os.getenv("TESTING", "false").lower() == "true" else "postgresql://localhost:5432/ocr_invoice")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

settings = Settings()