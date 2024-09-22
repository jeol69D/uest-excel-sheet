from fastapi import FastAPI
from app.routes import excel_routes, auth_routes
from app.config import settings  # Importar configuración
from app.middleware import ExceptionHandlerMiddleware
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

# Obtener la URI de MongoDB de las variables de entorno
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")


app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost:3000",  # URL de tu frontend
    "https://tudominio.com",   # URL de tu dominio en producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Añadir el middleware de manejo de excepciones
app.add_middleware(ExceptionHandlerMiddleware)

# Incluir rutas
app.include_router(excel_routes.router)
app.include_router(auth_routes.router)


# Ruta de prueba
@app.get("/")
def read_root():
    return {"message": "Excel Microservice is running"}

# Levantar la aplicación en el puerto configurado
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=settings.APP_PORT, reload=not settings.is_production)
