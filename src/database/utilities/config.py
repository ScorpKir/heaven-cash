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
