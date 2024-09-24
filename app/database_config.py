import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseConfig:
    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB: str = os.getenv("MONGO_DB", "excel_storage")

database_config = DatabaseConfig()
