"""
Описание модели операции
"""

__author__ = "Kirill Petryashev"

from sqlalchemy import Column, Integer, Text, Date, Numeric, ForeignKey, CheckConstraint
from ..utilities.database import Base


class Operation(Base):
    """
    Описание операции

    id - Целочисленный идентификатор операции
    user - Целочисленный идентификатор пользователя,
           совершившего операцию
    type - Тип операции
    date - Дата операции
    amount - Дополнительная информация
    """
    __tablename__ = "operations"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    user = Column("user", Integer, ForeignKey("user.id"), nullable=False)
    type = Column("type", Text, nullable=False)
    date = Column("date", Date, nullable=False)
    amount = Column("amount", Numeric, CheckConstraint("amount::numeric::integer > 0"), nullable=True)
