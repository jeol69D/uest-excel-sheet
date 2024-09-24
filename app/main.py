import logging
from fastapi import FastAPI
from app.routes import excel_routes, auth_routes
from app.app_config import app_config
from app.middleware import ExceptionHandlerMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.routes import user_routes  # Asegúrate de importar las rutas de usuario

# Configuración del logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = FastAPI()

# Configuración de CORS
origins = [
    "http://localhost:3000",  # URL de tu frontend
    "https://tudominio.com",   # URL de tu dominio en producción
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Añadir el middleware de manejo de excepciones
app.add_middleware(ExceptionHandlerMiddleware)

# Incluir rutas
app.include_router(excel_routes.router)
app.include_router(auth_routes.router)
app.include_router(user_routes.router)

# Ruta de prueba
@app.get("/")
def read_root():
    return {"message": "Excel Microservice is running"}

# Levantar la aplicación en el puerto configurado
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=app_config.APP_PORT, reload=not app_config.is_production)
