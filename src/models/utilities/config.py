"""
Логика получения переменных среды
"""

__author__ = "Kirill Petryashev"

import os
from dotenv import load_dotenv


def get_connection_string() -> str:
    """
    Получение строки подключения к базе данных
    из переменных среды

    :returns: Строка подключения
    :rtype: str
    """
    load_dotenv()
    connection_string = os.getenv("DB_CONNECTION")
    if connection_string is None:
        raise KeyError("Переменная DB_CONNECTION не задана!")
    return connection_string


def get_allowed_origins() -> list[str]:
    """
    Получение разрешенных источников для
    заголовков запроса CORS.
    :returns: Список разрешенных адресов
    :rtype: list[str]
    """

    load_dotenv()
    allowed = os.getenv("CORS_ALLOWED_ORIGINS")
    if allowed is None or allowed == "":
        raise KeyError("Не указан ни один разрешенный источник для CORS.")
    return allowed.split(',')
