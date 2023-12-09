"""
Юниттесты для операций
"""

__author__ = "Kirill Petryashev"

import unittest
import pytest
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.package.database.database import ENGINE
from app.package.database.models.operation import OperationDatabaseModel
from app.internal.models.operation import Operation


class TestUser(unittest.TestCase):
    """ Юнит-тесты для пользователя """

    @pytest.mark.excluded
    def test_add_many_operations(self):
        """
                Скрипт для заполнения базы данных пользователями
                """
        with Session(autoflush=False, bind=ENGINE) as db:
            truncate_query = text(f"""
                        TRUNCATE TABLE {OperationDatabaseModel.__tablename__} 
                        CASCADE;
                    """)
            connection = db.connection()
            connection.execute(truncate_query)
            db.commit()
        operations = [
            Operation(id=1,
                      user=1,
                      type="withdraw",
                      date=date.fromisoformat("2023-12-09"),
                      amount=100),
            Operation(id=2,
                      user=1,
                      type="deposit",
                      date=date.fromisoformat("2024-12-09"),
                      amount=1000),
            Operation(id=3,
                      user=1,
                      type="mobile",
                      date=date.fromisoformat("2023-12-11"),
                      amount=670,
                      additional="+79535117240"),
            Operation(id=4,
                      user=1,
                      type="communal",
                      date=date.fromisoformat("2023-11-21"),
                      amount=3456,
                      additional="3453456098345067034569"),
        ]
        for operation in operations:
            Operation.create(operation)

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
        id_ = 1
        operation = Operation.read_by_id(id_)
        self.assertEqual(id_, operation.id)

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
        id_ = 1
        result = Operation.delete(id_)
        self.assertEqual(result, True)
        operation = Operation(id=1,
                              user=1,
                              type="withdraw",
                              date=date.fromisoformat("2023-12-09"),
                              amount=100)
        Operation.create(operation)

    def test_delete_operation_by_non_existing_id(self):
        """
        Тестирование удаления операции по несуществующему идентификатору
        """
        id_ = 1_000_000_000
        operation = Operation.delete(id_)
        self.assertEqual(operation, False)
