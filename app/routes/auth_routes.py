from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import create_access_token
from app.database import user_collection 
from passlib.context import CryptContext
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

# Definir el contexto de hashing con bcrypt (el mismo que se usó al registrar)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para verificar la contraseña
def verify_hashed_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        # Verificar si se recibe el username en form_data
        if not form_data.username:
            logger.error(" ==> Username missing in form data")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username is required"
            )
        
        # Buscar al usuario en la base de datos
        user = await user_collection.find_one({"username": form_data.username})
        if not user:
            logger.warning(f" ==> User not found: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Verificar contraseña con passlib
        if not verify_hashed_password(form_data.password, user["hashed_password"]):
            logger.warning(f" ==> Incorrect password for user: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Generar el token de acceso
        access_token = create_access_token(data={"sub": user["username"], "user_id": str(user["_id"])})
        logger.info(f" ==> Token created successfully for user: {form_data.username}")

        return {"access_token": access_token, "token_type": "bearer"}
    
    except Exception as e:
        logger.error(f" ==> Error in /token endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error ==> {str(e)}")
