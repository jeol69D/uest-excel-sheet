from pydantic import BaseModel, root_validator
from typing import List, Dict, Any  # Se usa Any para aceptar cualquier tipo de dato
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class ExcelSheetModel(BaseModel):
    sheet_name: str
    columns: List[str]  # Los nombres de las columnas pueden ser cualquier cadena
    rows: List[Dict[str, Any]]  # Las filas pueden tener cualquier tipo de valor (str, int, float, datetime)

    # Validar que haya al menos una columna
    @root_validator(pre=True)
    def validate_columns_and_rows(cls, values):
        columns = values.get('columns')
        rows = values.get('rows')

        if not columns or len(columns) == 0:
            raise ValueError("Excel file must contain at least one column")

        # Validar que todas las filas tengan el mismo número de elementos que las columnas
        for row in rows:
            if len(row) != len(columns):
                raise ValueError(f"Row {row} does not match the number of columns {columns}")

        return values

    class Config:
        json_schema_extra = {
            "example": {
                "sheet_name": "Sheet1",
                "columns": ["Column1", "Column2", "Column3"],
                "rows": [
                    {"Column1": "Data1", "Column2": 100, "Column3": "2022-12-12"},
                    {"Column1": "Data2", "Column2": 150, "Column3": "2022-12-13"}
                ]
            }
        }
