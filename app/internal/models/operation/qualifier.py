"""
Инициализация типа операции
"""

__author__ = "Dmitry Voronin"

from datetime import date

from .operation import Operation
from .operation_types.deposit import DepositOperation
from .operation_types.withdraw import WithdrawOperation
from .operation_types.communal import CommunalPaymentOperation
from .operation_types.mobile import MobileOperation


class OperationTypeQualifier:
    """
    Определитель типа операции
    """
    operation: Operation = None

    def get_operation(self, user: int, operation_type: str, date_: date,
                      amount: float, additional: str) -> None:
        """Определение типа операции исходя из входных данных"""
        operation_type_mapping = {
            "deposit": DepositOperation,
            "withdraw": WithdrawOperation,
            "communal": CommunalPaymentOperation,
            "mobile": MobileOperation,
            "general": Operation
        }
        operation_class = operation_type_mapping[operation_type]
        self.operation = operation_class(user=user,
                                         date=date_,
                                         amount=amount,
                                         additional=additional)

    def execute(self) -> float:
        """
        Выполнение операции

        :return: Новое значение баланса пользователя если операция произошла
        :rtype: float | None
        """
        return self.operation.execute()
