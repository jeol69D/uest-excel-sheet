# app/models/user_model.py
from pydantic import BaseModel

class UserModel(BaseModel):
    id: str
    username: str
    hashed_password: str