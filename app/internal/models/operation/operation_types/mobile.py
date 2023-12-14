"""
Модель операции оплаты мобильной связи
"""

__author__ = "Alexey Kiselev"

from app.internal.models.operation.operation import Operation


class MobileOperation(Operation):
    """
    Операция оплаты мобильной связи

    user - Идентификатор пользователя, инициировавшего операцию
    type - Тип операции
    date - Дата операции
    amount - Сумма операции
    additional - Дополнительная информация (номер телефона) - обязательное поле
    """

    def __init__(self, user, date, amount, additional):
        if additional is None:
            raise ValueError("additional can not be None!")
        else:
            super().__init__(user=user,
                             date=date,
                             amount=amount,
                             additional=additional,
                             type='mobile')
            self.id = None

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
