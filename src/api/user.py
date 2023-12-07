"""
Эндпоинт /api/user/
"""

__author__ = "Kirill Petryashev"

from pydantic import ValidationError
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from src.models.user import \
    (User, read_user_id_by_code, read_user_by_id, update_user)

# Определение роутера для эндпоинтов пользователя
router = APIRouter(prefix='/user')


@router.get("/get_id")
async def get_user_id_by_code(code: str) -> JSONResponse:
    """
    # Получение идентификатора пользователя по ПИН-коду
    ## Параметры запроса
    ### `code` ПИН-код запрашиваемого пользователя.
     Например, `4579`, `1234`, `4200`, `0104`
    ## Примеры HTTP-запросов
    ### 1. `.../api/user/get_id?code=4579`
    ## Возможные ответы сервера
    `HTTP 200` Данные получены и переданы успешно.
    Вместе с этим кодом возвращается JSON в формате
    ```
    {
        "id": int
    }
    ```
    `HTTP 404` Пользователь с указанным ПИН-кодом **не существует**.
    """
    try:
        id_ = read_user_id_by_code(code)
        if id_ is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Неизвестный ПИН-код")
        # id_ = "" if id_ is None else id_
        response = {"id": id_}
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Неверный формат пин-кода")


@router.get("/get", response_model=User)
async def get_user(id: int | None = None) -> JSONResponse:
    """
    # Получение данных пользователя по идентификатору
    ## Параметры запроса
    ### `id` Идентификатор запрашиваемого пользователя.
     Например, `1`, `2`, `5`, `10`
    ## Примеры HTTP-запросов
    ### 1. `.../api/user/get?id=3`
    ## Возможные ответы сервера
    `HTTP 200` Данные получены и переданы успешно.
    Вместе с этим кодом возвращается JSON в формате
    ```
    {
        "id": int,
        "code": string,
        "card_number": string,
        "payment_system": string,
        "balance": int
    }
    ```
    `HTTP 404` Пользователь с указанным идентификатором **не существует**.
    """
    try:
        response = read_user_by_id(id)
        if response is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Неизвестный ID")
        return JSONResponse(content=response.model_dump(),
                            status_code=status.HTTP_200_OK)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Неверный формат входных данных")


@router.post("/operation")
async def user_operation(id: int,
                         amount: float,
                         type: str | None = "general") -> JSONResponse:
    """
    # Обработка операции пользователя с указанным идентификатором
    ## Параметры запроса
    ### `id` Идентификатор пользователя, с которым проводится операция.
     Например, `1`, `2`, `5`, `10`
    ### `amount` Изменение баланса пользователя.
     Например, `100`, `5000`, `-250`, `-1100`
    ### `type` Название типа операции.
     Например, `withdraw` (снятие), `deposit` (внесение), `mobile`
     (мобильная связь), `communal` (коммунальные платежи).
     Тип операции должен быть согласован со знаком числа amount: нельзя
     указывать тип "снятие" с положительным amount и т.п.
    ### `!` Если тип операции не указан, по умолчанию будет выбрано "general".
    ## Примеры HTTP-запросов
    ### 1. `.../api/user/operation?id=3&amount=1000&type=deposit`
    ### 2. `.../api/user/operation?id=5&amount=-500&type=withdraw`
    ### 3. `.../api/user/operation?id=5&amount=-300`
    ## Возможные ответы сервера
    `HTTP 200` Операция проведена успешно.
    Вместе с этим кодом возвращается JSON с новым балансом в формате
    ```
    {
        "balance": float
    }
    ```
    `HTTP 500` Операция не прошла, а баланс не изменен, так как у пользователя
    **недостаточно средств**.
    ```
    `HTTP 404` Пользователь с указанным идентификатором **не существует**.
    """

    # TODO:
    #   1. Добавление операции в базу данных.
    #   2. Обработка исключительных случаев типа "указан тип withdraw,
    #       но значение amount положительно" и наоборот.
    #   3. Возврат кодов состояния или информации в JSON для информирования
    #       фронтенда о статусе запроса.

    try:
        user = read_user_by_id(id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Неизвестный ID")
        try:
            user.balance += amount
            update_user(user)
            response = {"balance": user.balance}
        except ValidationError:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            raise HTTPException(status_code=status_code,
                                detail="Не хватает денег")
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Неверный формат входных данных")
