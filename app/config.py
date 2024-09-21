# app/config.py

import os
from dotenv import load_dotenv

# Cargar el archivo .env
load_dotenv()

class Settings:
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB: str = os.getenv("MONGO_DB", "excel_storage")
    APP_PORT: int = int(os.getenv("APP_PORT", 8000))
    APP_ENV: str = os.getenv("APP_ENV", "development")
    
    @property
    def is_production(self) -> bool:
        return self.APP_ENV == "production"

settings = Settings()
