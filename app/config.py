# app/config.py

from app.database_config import database_config
from app.app_config import app_config

# Opcional: Imprimir la configuración para verificar
if __name__ == "__main__":
    print("Database Config:", database_config.__dict__)
    print("App Config:", app_config.__dict__)
