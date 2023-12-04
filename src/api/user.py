"""
Ендпоинт /api/user/
"""

__author__ = "Kirill Petryashev"

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from src.models.user import User, read_user_id_by_code, read_user_by_id

# Определение роутера для ендпоинтов пользователя
router = APIRouter(prefix='/user')


@router.get("/get_user_id")
async def get_user_id_by_code(code: str) -> JSONResponse:
    """
    Получение идентификатора пользователя по пин-коду
    """
    try:
        id_ = read_user_id_by_code(code)
        id_ = "" if id_ is None else id_
        response = {"id": id_}
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Неверный формат пин-кода")


@router.get("/get", response_model=User)
async def get_user(id: int | None = None) -> JSONResponse:
    """
    Получение данных пользователя по пинкоду или идентификатору
    """
    response = read_user_by_id(id)
    return JSONResponse(content=response.model_dump(),
                        status_code=status.HTTP_200_OK)
