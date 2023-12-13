"""
Модель операции оплаты коммунальных платежей
"""

__author__ = "Alexey Kiselev"

from app.internal.models.operation.operation import Operation, OperationTypes


class CommunalPaymentOperation(Operation):
    """
    Операция оплаты коммунальных платежей

    user - Идентификатор пользователя, инициировавшего операцию
    type - Тип операции
    date - Дата операции
    amount - Сумма операции
    additional - Дополнительная информация (номер квитанции) - обязательное поле
    """

    def __init__(self, id, user, date, amount, additional):
        if additional is None:
            raise ValueError("additional can not be None!")
        else:
            super().__init__(id=id,
                             user=user,
                             date=date,
                             amount=amount,
                             additional=additional,
                             type='communal')

    def __setattr__(self, name, value):
        """
        Запрет на изменение поля type

        :param name: имя поля, изменение которого отслеживаем
        :param value: значение отслеживаемого поля
        """
        if name == 'type' and value != 'communal':
            raise ValueError("Can`t change type of operation")
        else:
            super().__setattr__(name, value)
