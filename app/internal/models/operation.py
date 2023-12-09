"""
Описание модели операции
"""

__author__ = "Kirill Petryashev"

from typing import Optional
from enum import Enum
from datetime import datetime
from sqlalchemy import Column, Integer, Text, Date, Numeric, ForeignKey
from pydantic import BaseModel, ConfigDict, confloat, conint

from app.package.database.database import Base


class OperationTypes(str, Enum):
    """
    Перечисление стандартных типов операций
    """
    WITHDRAW = 'withdraw'
    DEPOSIT = 'deposit'
    MOBILE = 'mobile'
    COMMUNAL = 'communal'


class OperationDatabaseModel(Base):
    """
    Модель операции для базы данных
    """
    __tablename__ = "operations"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    user = Column("user", Integer, ForeignKey("user.id"), nullable=False)
    type = Column("type", Text, nullable=False)
    date = Column("date", Date, nullable=False)
    amount = Column("amount", Numeric, nullable=True)
    additional = Column("additional", Text)

    def to_dict(self) -> dict:
        """
        Преобразование модели к словарю

        :returns: Словарь с необходимыми полями
        :rtype: dict
        """
        return {
            "id": self.id,
            "user": self.user,
            "type": self.type,
            "date": self.date,
            "amount": self.amount,
            "additional": self.additional
        }


class Operation(BaseModel):
    """
    Описание операции

    user - Идентификатор пользователя, инициировавшего операцию
    type - Тип операции
    date - Дата операции
    amount - Сумма операции
    additional - Дополнительная информация
    """

    model_config = ConfigDict(validate_assignment=True)

    id: Optional[conint(ge=1)] = None
    type: OperationTypes
    date: datetime
    amount: confloat(ge=0.00)
    additional: str
