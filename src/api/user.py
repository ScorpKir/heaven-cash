"""
Ендпоинт /api/user/
"""

__author__ = "Kirill Petryashev"

import pydantic
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from src.models.user import \
    (User, read_user_id_by_code, read_user_by_id, update_user)

# Определение роутера для ендпоинтов пользователя
router = APIRouter(prefix='/user')


@router.get("/get_id")
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

@router.post("/update_balance")
async def user_update_balance(id: int, amount: int) -> JSONResponse:
    """
    # Изменение баланса пользователя по его идентификатору
    ## Возможные ответы сервера
    `HTTP 200` Баланс изменен успешно.
    Вместе с этим кодом возвращается JSON с новым балансом в формате
    ```
    {
        "balance": string
    }
    ```
    `HTTP 418` Баланс не изменен, так как у пользователя
    **недостаточно средств**.
    Вместе с этим кодом возвращается JSON с сообщением **"unchanged"**
    в формате
    ```
    {
        "balance": "unchanged"
    }
    ```
    """
    user = read_user_by_id(id)
    response = {"balance": "unchanged"}
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Неизвестный ID")
    try:
        user.balance += amount
        update_user(user)
        response = {"balance": str(user.balance)}
    except pydantic.ValidationError:
        return JSONResponse(content=response,
                            status_code=status.HTTP_418_IM_A_TEAPOT)
    return JSONResponse(content=response,
                        status_code=status.HTTP_200_OK)
