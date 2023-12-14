"""
Описание модели операции
"""

__author__ = "Kirill Petryashev"

from typing import Optional
from enum import Enum
from datetime import date
from pydantic import BaseModel, ConfigDict, confloat, conint

from app.package.database.models.operation import OperationDatabaseModel
from app.internal.models.user.user import User


class OperationTypes(str, Enum):
    """
    Перечисление стандартных типов операций
    """
    WITHDRAW = 'withdraw'
    DEPOSIT = 'deposit'
    MOBILE = 'mobile'
    COMMUNAL = 'communal'


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
    user: conint(ge=1)
    type: OperationTypes
    date: date
    amount: confloat(ge=0.00)
    additional: Optional[str] = None

    def __to_database_model(self) -> OperationDatabaseModel:
        """
        Конвертация модели операции
        в модель для базы данных

        :returns: Модель операции для базы данных
        :rtype: OperationDatabaseModel
        """
        return OperationDatabaseModel(**self.model_dump())

    @classmethod
    def create(cls, operation) -> int:
        """
        Добавление операции

        :param operation: Операция для создания
        :type operation: Operation

        :returns: Идентификатор созданной операции
        :rtype: int
        """
        return OperationDatabaseModel.create(operation.__to_database_model())

    @classmethod
    def read_by_id(cls, id_: int):
        """
        Чтение операции по идентификатору

        :param id_: Идентификатор операции
        :type id_: int

        :returns: Операция или ничего, в случае если
                  операция не будет найдена
        :rtype: Operation | None
        """
        db_operation = OperationDatabaseModel.read_by_id(id_)
        if db_operation:
            return cls.model_validate(db_operation.to_dict())

    @classmethod
    def delete(cls, id_: int) -> bool:
        """
        Удаление операции

        :param id_: Идентификатор операции для удаления
        :type id_: int

        :returns: Логическое значение обозначающее успех операции
        :rtype: bool
        """
        return OperationDatabaseModel.delete(id_)
      
    def execute(self):
        """
        Выполнение операции

        :return: Логическое значение обозначающее успех операции
        :rtype: bool
        """

        user = User.read_by_id(self.user)
        user.balance -= self.amount
        User.update(user)
        self.id = Operation.create(self)
        return self.id is not None

    def undo(self):
        """
        Отмена операции

        :return: Логическое значение обозначающее успех операции
        :rtype: bool
        """
        if self.id:
            user = User.read_by_id(self.user)
            user.balance += self.amount
            User.update(user)
            return Operation.delete(self.id)
        else:
            raise ValueError("Нельзя отменить не выполненную операцию")
