"""
Модель операции внесения средств
"""

__author__ = "Alexey Kiselev"

from app.internal.models.operation.operation import Operation, OperationTypes
from app.internal.models.user.user import User


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

    def execute(self):
        """
        Выполнение внесения средств

        :return: id пользователя который выполнил операцию
        :rtype: int
        """

        user = User.read_by_id(self.user)
        user.balance += self.amount
        User.update(user)
        # Занесение операции в базу данных
        _id = Operation.create(self)
        return _id

    def undo(self):
        """
        Отмена внесения средств

        :return: Логическое значение обозначающее успех операции
        :rtype: bool
        """
        user = User.read_by_id(self.user)
        user.balance -= self.amount
        User.update(user)
        # Удаление операции из базы данных
        return Operation.delete(self.id)
