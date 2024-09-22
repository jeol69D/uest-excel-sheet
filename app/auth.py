# app/auth.py
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.database import user_collection  
from app.models.user_model import UserModel


SECRET_KEY = "your_secret_key"  # Cambia esto por un valor más seguro
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Aquí puedes implementar funciones para crear y verificar usuarios

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Implementa la función para obtener el usuario
async def get_user(username: str) -> UserModel:
    user_data = await user_collection.find_one({"username": username})  # Busca en tu base de datos
    if user_data:
        return UserModel(id=str(user_data["_id"]), username=user_data["username"], hashed_password=user_data["hashed_password"])
    return None

