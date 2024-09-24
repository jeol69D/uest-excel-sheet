import os
from dotenv import load_dotenv

load_dotenv()

class AppConfig:
    APP_PORT: int = int(os.getenv("APP_PORT", 8000))
    APP_ENV: str = os.getenv("APP_ENV", "development")

    @property
    def is_production(self) -> bool:
        return self.APP_ENV.lower() == "production"

app_config = AppConfig()
