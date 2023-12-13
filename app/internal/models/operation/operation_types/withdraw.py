"""
Модель операции снятия средств
"""

__author__ = "Alexey Kiselev"

from app.internal.models.operation.operation import Operation, OperationTypes


class WithdrawOperation(Operation):
    """
    Операция снятия средств

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
                         type='withdraw')
        self.type = 'withdraw'

    def __setattr__(self, name, value):
        """
        Запрет на изменение поля type

        :param name: имя поля, изменение которого отслеживаем
        :param value: значение отслеживаемого поля
        """
        if name == 'type' and value != 'withdraw':
            raise ValueError("Can`t change type of operation")
        else:
            super().__setattr__(name, value)
