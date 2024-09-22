# app/routes/auth_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.auth import create_access_token, verify_password
from app.models.user_model import UserModel  # Asegúrate de tener un modelo de usuario
from app.database import user_collection  # Colección de usuarios en tu base de datos
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await user_collection.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Si el usuario es válido, crea y devuelve un token
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}
