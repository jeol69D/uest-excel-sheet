# app-middleware.py
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.logging_config import logger

class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except HTTPException as ex:
            logger.error(f"HTTP Exception: {ex.detail}")
            return JSONResponse(
                status_code=ex.status_code,
                content={"detail": ex.detail},
            )
        except Exception as ex:
            logger.error(f"Unhandled Exception: {str(ex)}")
            return JSONResponse(
                status_code=500,
                content={"detail": "An internal server error occurred."}
            )
