"""
Модель операции снятия средств
"""

__author__ = "Alexey Kiselev"

from app.internal.models.operation.operation import Operation


class WithdrawOperation(Operation):
    """
    Операция снятия средств

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
                         type='withdraw')
        self.id = None

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
