"""
Модель операции внесения средств
"""

__author__ = "Alexey Kiselev"

from app.internal.models.operation.operation import Operation
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

    def __init__(self, user, date, amount, additional=None):
        super().__init__(user=user,
                         date=date,
                         amount=amount,
                         additional=additional,
                         type='deposit')
        self.id = None

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

    def execute(self) -> float:
        """
        Выполнение операции внесения средств

        :return: Новое значение баланса пользователя если операция произошла
        :rtype: float | None
        """
        user = User.read_by_id(self.user)
        if user:
            user.balance += self.amount
            User.update(user)
            self.id = Operation.create(self)
            return user.balance

    def undo(self) -> bool:
        """
        Отмена внесения средств

        :return: Логическое значение обозначающее успех операции
        :rtype: bool
        """
        if self.id:
            user = User.read_by_id(self.user)
            user.balance -= self.amount
            User.update(user)
            return Operation.delete(self.id)
        else:
            raise ValueError("Нельзя отменить не выполненную операцию")
