"""
Модель операции оплаты мобильной связи
"""

__author__ = "Alexey Kiselev"

from app.internal.models.operation.operation import Operation, OperationTypes


class MobileOperation(Operation):
    """
    Операция оплаты мобильной связи

    user - Идентификатор пользователя, инициировавшего операцию
    type - Тип операции
    date - Дата операции
    amount - Сумма операции
    additional - Дополнительная информация (номер телефона) - обязательное поле
    """
    def __init__(self, id, user, date, amount, additional):
        super().__init__(id=id,
                         user=user,
                         date=date,
                         amount=amount,
                         additional=additional,
                         type='mobile')
        self.type = 'mobile'
        if additional is not None:
            self.additional = additional
        else:
            raise ValueError("additional can not be None!")

    def __setattr__(self, name, value):
        """
        Запрет на изменение поля type.

        :param name: имя поля, изменение которого отслеживаем
        :param value: значение отслеживаемого поля
        """
        if name == 'type' and value != 'mobile':
            raise ValueError("Can`t change type of operation")
        else:
            super().__setattr__(name, value)
