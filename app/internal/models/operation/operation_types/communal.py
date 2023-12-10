"""
Модель операции оплаты коммунальных платежей
"""

__author__ = "Alexey Kiselev"

from app.internal.models.operation.operation import Operation


class CommunalPaymentOperation(Operation):
    """
    Операция оплаты коммунальных платежей
    """
    ...
