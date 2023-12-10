"""
Модель операции внесения средств
"""

__author__ = "Alexey Kiselev"

from app.internal.models.operation.operation import Operation


class CommunalPaymentOperation(Operation):
    """
    Операция внесения средств
    """
    ...