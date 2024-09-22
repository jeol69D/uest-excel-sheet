# app/database.py
import motor.motor_asyncio
from app.config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGO_URI)
database = client[settings.MONGO_DB]

excel_collection = database.get_collection("excel_sheets")
user_collection = database.get_collection("users")  
