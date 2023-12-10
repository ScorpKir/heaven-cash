"""
Модель операции снятия средств
"""

__author__ = "Alexey Kiselev"

from app.internal.models.operation.operation import Operation


class WithdrawOperation(Operation):
    """
    Операция снятия средств
    """
    ...