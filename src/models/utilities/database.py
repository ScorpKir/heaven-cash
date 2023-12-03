"""
Логика управления базой данных
"""

__author__ = "Kirill Petryashev"

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from .config import get_connection_string

# Строка подключения к базе данных
DATABASE_URL = get_connection_string()

# Движок подключения к базе данных
ENGINE = create_engine(DATABASE_URL)


# Базовая модель
class Base(DeclarativeBase):
    pass


def init_database() -> None:
    """
    Создание базы данных и всех её таблиц
    """
    Base.metadata.create_all(bind=ENGINE)
