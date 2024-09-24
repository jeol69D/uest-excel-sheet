# app/database.py
from app.database_config import database_config
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(database_config.MONGO_URI)
database = client[database_config.MONGO_DB]

excel_collection = database.get_collection("excel_sheets")
user_collection = database.get_collection("users")  
