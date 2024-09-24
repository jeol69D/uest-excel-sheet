from fastapi import APIRouter, UploadFile, HTTPException, Depends
from app.database import excel_collection
from app.models.excel_model import ExcelSheetModel
from app.auth import oauth2_scheme, get_user
from app.utils.excel_processor import process_excel
from pydantic import ValidationError
import logging
import hashlib
import traceback

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter()

def calculate_file_hash(file_content: bytes):
    hasher = hashlib.sha256()
    hasher.update(file_content)
    return hasher.hexdigest()

@router.post("/upload-excel", status_code=201)
async def upload_excel(file: UploadFile, token: str = Depends(oauth2_scheme)):
    if file.content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        raise HTTPException(status_code=400, detail="Invalid file type. Only Excel files are allowed.")

    user = await get_user(token)
    if user is None:
        raise HTTPException(status_code=403, detail="Could not validate credentials.")

    try:
        file_content = await file.read()
        file_hash = calculate_file_hash(file_content)

        existing_file = await excel_collection.find_one({"file_hash": file_hash})
        if existing_file:
            raise HTTPException(status_code=400, detail="This Excel file has already been uploaded.")

        excel_data = process_excel(file_content)

        excel_model = ExcelSheetModel(**excel_data)

        result = await excel_collection.insert_one({
            **excel_model.dict(),
            "file_hash": file_hash
        })

        return {"message": "Excel sheet uploaded successfully", "id": str(result.inserted_id)}

    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=f"Data validation error: {ve}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
