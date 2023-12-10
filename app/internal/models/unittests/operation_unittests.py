"""
Юниттесты для операций
"""

__author__ = "Kirill Petryashev"

import unittest
from datetime import date

from app.internal.models.operation.operation import Operation


class TestUser(unittest.TestCase):
    """ Юнит-тесты для пользователя """

    def test_create_user(self):
        """
        Тестирование создания операции
        """
        operation = Operation(id=5,
                              user=1,
                              type="communal",
                              date=date.fromisoformat("2023-11-21"),
                              amount=3456,
                              additional="3453456098345067034569")
        id_ = Operation.create(operation)
        self.assertNotEqual(id_, None)
        Operation.delete(id_)

    def test_read_operation_by_id(self):
        """
        Тестирование чтения операции
        """
        operation = Operation(id=5,
                              user=1,
                              type="communal",
                              date=date.fromisoformat("2023-11-21"),
                              amount=3456,
                              additional="3453456098345067034569")
        Operation.create(operation)
        id_ = operation.id
        new_operation = Operation.read_by_id(id_)
        self.assertNotEqual(new_operation, None)
        Operation.delete(id_)

    def test_read_operation_by_non_existing_id(self):
        """
        Тестирование чтения операции по несуществующему идентификатору
        """
        id_ = 1_000_000_000
        operation = Operation.read_by_id(id_)
        self.assertEqual(operation, None)

    def test_delete_operation(self):
        """
        Тестирование удаления операции
        """
        operation = Operation(id=5,
                              user=1,
                              type="communal",
                              date=date.fromisoformat("2023-11-21"),
                              amount=3456,
                              additional="3453456098345067034569")
        Operation.create(operation)
        result = Operation.delete(operation.id)
        self.assertEqual(result, True)

    def test_delete_operation_by_non_existing_id(self):
        """
        Тестирование удаления операции по несуществующему идентификатору
        """
        id_ = 1_000_000_000
        operation = Operation.delete(id_)
        self.assertEqual(operation, False)
