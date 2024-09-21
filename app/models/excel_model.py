# app/models/excel_model.py
from pydantic import BaseModel, validator
from typing import List

class ExcelSheetModel(BaseModel):
    sheet_name: str
    columns: List[str]
    rows: List[dict]

    @validator('columns')
    def validate_columns(cls, v):
        if len(v) == 0:
            raise ValueError("Excel file must contain at least one column")
        return v

    @validator('rows', each_item=True)
    def validate_rows(cls, v, values):
        if len(v) != len(values.get('columns')):
            raise ValueError("Row does not match the number of columns")
        return v

    class Config:
        schema_extra = {
            "example": {
                "sheet_name": "Sheet1",
                "columns": ["Name", "Age", "City"],
                "rows": [
                    {"Name": "John", "Age": 30, "City": "New York"},
                    {"Name": "Jane", "Age": 25, "City": "Los Angeles"},
                ]
            }
        }
