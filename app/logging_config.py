# app/logging_config.py
import logging

# Configuración básica de logging
logging.basicConfig(
    filename='app.log',  # Guardar los logs en un archivo
    level=logging.INFO,  # Nivel de logging
    format='%(asctime)s - %(levelname)s - %(message)s',  # Formato del log
)

logger = logging.getLogger(__name__)
