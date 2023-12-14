"""
Инициализация типа операции
"""

__author__ = "Dmitry Voronini"

from datetime import date

from operation import Operation
from operation_types.deposit import DepositOperation
from operation_types.withdraw import WithdrawOperation
from operation_types.communal import CommunalPaymentOperation
from operation_types.mobile import MobileOperation


class OperationTypeQualifier:
    """
    Определитель типа операции
    """
    operation: Operation = None

    @classmethod
    def get_operation(cls, user: int, operation_type: str, date_: date,
                      amount: float, additional: str) -> None:
        """Определение типа операции исходя из входных данных"""
        operation_type_mapping = {
            "deposit": DepositOperation,
            "withdraw": WithdrawOperation,
            "communal": CommunalPaymentOperation,
            "mobile": MobileOperation
        }
        operation_class = operation_type_mapping[operation_type]
        cls.operation = operation_class(user=user,
                                        type=operation_type,
                                        date=date_,
                                        amount=amount,
                                        additional=additional)

    @classmethod
    def execute(cls) -> None:
        """Выполнение операции"""
        return cls.operation.execute()
