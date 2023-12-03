"""
Ендпоинт /api/user/
"""

__author__ = "Kirill Petryashev"

from fastapi import APIRouter, Body, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from src.models.user import User, read_user_by_code

# Определение роутера для ендпоинтов пользователя
router = APIRouter(prefix='/user')


@router.get("/get", response_model=User)
async def get_user(code: str = Body(embed=True)) -> JSONResponse:
    """
    Получение данных пользователя по пинкоду
    """
    try:
        response = read_user_by_code(code)
        return JSONResponse(content=response.model_dump(),
                            status_code=status.HTTP_200_OK)
    except ValueError:
        raise HTTPException(status_code=500, detail="Invalid pincode format")
