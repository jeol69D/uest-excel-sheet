# app/models/user_model.py
from pydantic import BaseModel, Field
from bson import ObjectId

class UserModel(BaseModel):
    username: str
    hashed_password: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
