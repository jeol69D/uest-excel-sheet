from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user_model import UserModel
from app.database import user_collection
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from bson import ObjectId
from passlib.context import CryptContext

router = APIRouter()

# Definir el contexto de hashing con bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Función para generar el hash de la contraseña
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Función para verificar la contraseña con el hash
def verify_hashed_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Modelo para el registro de usuario
class UserRegisterModel(BaseModel):
    username: str
    password: str

# Modelo para la actualización de usuario
class UserUpdateModel(BaseModel):
    username: str = None
    password: str = None

@router.post("/users/register", status_code=status.HTTP_201_CREATED)
async def register_user(user: UserRegisterModel):
    # Verificar si el usuario ya existe
    existing_user = await user_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered.")
    
    # Hashear la contraseña del usuario
    hashed_password = hash_password(user.password)

    new_user = {
        "username": user.username,
        "hashed_password": hashed_password  # Guardar el hash en lugar de la contraseña en texto plano
    }
    
    result = await user_collection.insert_one(new_user)
    return {"id": str(result.inserted_id), "username": user.username}

@router.get("/users/{user_id}", response_model=UserModel)
async def get_user(user_id: str):
    user_data = await user_collection.find_one({"_id": ObjectId(user_id)})
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found.")
    
    return UserModel(id=str(user_data["_id"]), username=user_data["username"], hashed_password=user_data["hashed_password"])

@router.put("/users/{user_id}", response_model=UserModel)
async def update_user(user_id: str, user_update: UserUpdateModel):
    update_data = {}
    
    if user_update.username:
        update_data["username"] = user_update.username
    if user_update.password:
        # Hashear la nueva contraseña
        update_data["hashed_password"] = hash_password(user_update.password)
    
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided.")
    
    result = await user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found.")
    
    updated_user = await user_collection.find_one({"_id": ObjectId(user_id)})
    return UserModel(id=str(updated_user["_id"]), username=updated_user["username"], hashed_password=updated_user["hashed_password"])

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    result = await user_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found.")

@router.get("/users", response_model=list[UserModel])
async def list_users():
    users_cursor = user_collection.find()
    users = await users_cursor.to_list(length=100)  # Cambia el número según sea necesario
    return [UserModel(id=str(user["_id"]), username=user["username"], hashed_password=user["hashed_password"]) for user in users]

@router.post("/users/{user_id}/change-password")
async def change_password(user_id: str, form_data: OAuth2PasswordRequestForm = Depends()):
    user_data = await user_collection.find_one({"_id": ObjectId(user_id)})
    if not user_data or not verify_hashed_password(form_data.password, user_data["hashed_password"]):
        raise HTTPException(status_code=403, detail="Invalid credentials.")
    
    # Hashear la nueva contraseña
    hashed_new_password = hash_password(form_data.password)
    
    await user_collection.update_one({"_id": ObjectId(user_id)}, {"$set": {"hashed_password": hashed_new_password}})
    
    return {"message": "Password updated successfully."}
