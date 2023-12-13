"""
Инициализация типа операции
"""

__author__ = "Dmitry Voronini"

from operation import Operation, OperationTypes


class OperationTypeQualifier:
    @classmethod
    def get_operation(cls, user, operation_type, date, amount, additional):
        if operation_type == OperationTypes.COMMUNAL:
            if additional is None:
                raise ValueError("NullPointerException")
            return Operation(user=user, type=operation_type, date=date,
                             amount=amount, additional=additional)
        elif operation_type == OperationTypes.MOBILE:
            if additional is None:
                raise ValueError("NullPointerException")
            return Operation(user=user, type=operation_type, date=date,
                             amount=amount, additional=additional)
        else:
            return Operation(user=user, type=operation_type, date=date,
                             amount=amount)

    @classmethod
    def execute(cls, operations):
        operation = Operation.create(operations)
        return operation
