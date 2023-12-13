"""
Модель операции внесения средств
"""

__author__ = "Alexey Kiselev"

from app.internal.models.operation.operation import Operation, OperationTypes
import app.internal.routes.user as ruser


class DepositOperation(Operation):
    """
    Операция внесения средств

    user - Идентификатор пользователя, инициировавшего операцию
    type - Тип операции
    date - Дата операции
    amount - Сумма операции
    additional - Дополнительная информация
    """

    def __init__(self, id, user, date, amount, additional=None):
        super().__init__(id=id,
                         user=user,
                         date=date,
                         amount=amount,
                         additional=additional,
                         type='deposit')
        self.type = 'deposit'

    def __setattr__(self, name, value):
        """
        Запрет на изменение поля type

        :param name: имя поля, изменение которого отслеживаем
        :param value: значение отслеживаемого поля
        """
        if name == 'type' and value != 'deposit':
            raise ValueError("Can`t change type of operation")
        else:
            super().__setattr__(name, value)

    @classmethod
    def execute(cls):
        """
        Выполнение внесения средств

        :return: id пользователя который выполнил операцию
        :rtype: int
        """

        # Обработка операции пользователя с указанным идентификатором
        ruser.user_operation(cls.user, cls.amount, 'deposit')

        # Занесение операции в базу данных
        _id = Operation.create(cls)
        return _id

    @classmethod
    def undo(cls):
        """
        Отмена внесения средств

        :return: Логическое значение обозначающее успех операции
        :rtype: bool
        """
        # Обработка операции пользователя с указанным идентификатором
        ruser.user_operation(cls.user, -cls.amount, 'deposit')
        # Удаление операции из базы данных
        return Operation.delete(cls.id)
