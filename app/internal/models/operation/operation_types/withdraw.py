"""
Модель операции снятия средств
"""

__author__ = "Alexey Kiselev"

from app.internal.models.operation.operation import Operation, OperationTypes
import app.internal.routes.user as ruser


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

    @classmethod
    def execute(cls):
        """
        Выполнение снятия средств

        :return: id пользователя который выполнил операцию
        :rtype: int
        """

        # Обработка операции пользователя с указанным идентификатором
        ruser.user_operation(cls.user, -cls.amount, 'withdraw')
        # Занесение операции в базу данных
        _id = Operation.create(cls)
        return _id

    @classmethod
    def undo(cls):
        """
        Отмена снятия средств

        :return: Логическое значение обозначающее успех операции
        :rtype: bool
        """
        # Обработка операции пользователя с указанным идентификатором
        ruser.user_operation(cls.user, cls.amount, 'withdraw')
        # Удаление операции из базы данных
        return Operation.delete(cls.id)
