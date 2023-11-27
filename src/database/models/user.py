"""
Описание модели пользователя
"""

__author__ = "Kirill Petryashev"

from sqlalchemy import Column, Integer, Text
from ..utilities.database import Base


class User(Base):
    """
    Описание пользователя

    id - Целочисленный идентификатор пользователя
    code - Пин-код пользователя для банкомата
    balance - Количество денег на счёте пользователя
    """
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(Text, nullable=False)
    balance = Column(Integer, default=0)
