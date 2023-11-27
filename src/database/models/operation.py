"""
Описание модели операции
"""

__author__ = "Kirill Petryashev"

from sqlalchemy import Column, Integer, Text, Date, ForeignKey
from ..utilities.database import Base


class Operation(Base):
    """
    Описание операции

    id - Целочисленный идентификатор операции
    user - Целочисленный идентификатор пользователя,
           совершившего операцию
    type - Тип операции
    date - Дата операции
    additional - Дополнительная информация
    """
    __tablename__ = "operations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(Integer, ForeignKey("user.id"), nullable=False)
    type = Column(Text, nullable=False)
    date = Column(Date, nullable=False)
    additional = Column(Text, nullable=True)
