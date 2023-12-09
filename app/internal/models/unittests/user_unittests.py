"""
Юниттесты для пользователя
"""

__author__ = "Kirill Petryashev"

import unittest
import pytest
from random import randint
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

from app.package.database.database import ENGINE
from app.package.database.models.user import UserDatabaseModel
from app.internal.models.user import User


class TestUser(unittest.TestCase):
    """ Юнит-тесты для пользователя """

    @pytest.mark.excluded
    def test_add_many_users(self):
        """
        Скрипт для заполнения базы данных пользователями
        """
        with Session(autoflush=False, bind=ENGINE) as db:
            truncate_query = text(f"""
                TRUNCATE TABLE {UserDatabaseModel.__tablename__} CASCADE;
            """)
            connection = db.connection()
            connection.execute(truncate_query)
            db.commit()
        users = [
            User(id=1,
                 code="4579",
                 card_number="1677",
                 payment_system="МастерМир",
                 balance=10_000),
            User(id=2,
                 code="5243",
                 card_number="1115",
                 payment_system="ЯрВиза",
                 balance=56_780),
            User(id=3,
                 code="1093",
                 card_number="5641",
                 payment_system="ПудовичокПэй",
                 balance=1_423_000),
            User(id=4,
                 code="8850",
                 card_number="2845",
                 payment_system="МастерМир",
                 balance=345_987),
            User(id=5,
                 code="5985",
                 card_number="5110",
                 payment_system="ПудовичокПэй",
                 balance=777_777),
            User(id=6,
                 code="4731",
                 card_number="0378",
                 payment_system="КубышкаПэй",
                 balance=14_536),
            User(id=7,
                 code="7656",
                 card_number="2335",
                 payment_system="СлавКард",
                 balance=100),
            User(id=8,
                 code="9695",
                 card_number="0244",
                 payment_system="МастерМир",
                 balance=156),
            User(id=9,
                 code="8691",
                 card_number="0434",
                 payment_system="ЯрВиза",
                 balance=789_564),
            User(id=10,
                 code="9117",
                 card_number="6234",
                 payment_system="МастерМир",
                 balance=43_456)
        ]
        for user in users:
            User.create(user)

    def test_create_user(self):
        """
        Тестирование создания пользователя
        """
        user = User(code="8543",
                    card_number="5754",
                    payment_system="МастерМир",
                    balance=12345)
        id_ = User.create(user)
        self.assertNotEqual(id_, None)
        user.delete(id_)

    def test_read_user_by_id(self):
        """
        Тестирование чтения пользователя
        """
        id_ = 1
        user = User.read_by_id(id_)
        self.assertEqual(id_, user.id)

    def test_read_user_by_non_existing_id(self):
        """
        Тестирование чтения пользователя по несуществующему идентификатору
        """
        id_ = 11
        user = User.read_by_id(id_)
        self.assertEqual(user, None)

    def test_read_user_by_correct_code(self):
        code = "4579"
        user = User.read_by_code(code)
        self.assertEqual(code, user.code)

    def test_read_user_by_non_existing_code(self):
        """
        Тестирование чтения пользователя по несуществующему пинкоду
        """
        code = "5754"
        user = User.read_by_code(code)
        self.assertEqual(user, None)

    def test_read_user_id_by_correct_code(self):
        """
        Тестирование чтения идентификатора пользователя по корректному пинкоду
        """
        code = "4579"
        id_ = User.read_id_by_code(code)
        self.assertNotEqual(id_, None)

    def test_read_user_id_by_broken_code(self):
        """
        Тестирование чтения идентификатора пользователя по некорректному пинкоду
        """
        code = "a"
        self.assertRaises(ValueError, User.read_id_by_code, code)

    def test_read_user_id_by_non_existing_code(self):
        """
        Тестирование чтения идентификатора пользователя
        по несуществующему пинкоду
        """
        code = "5754"
        id_ = User.read_id_by_code(code)
        self.assertEqual(id_, None)

    def test_read_user_by_broken_code(self):
        code = "asdf"
        self.assertRaises(ValueError, User.read_by_code, code)

    def test_update_user(self):
        """
        Тестирование обновления пользователя
        """
        id_ = 1
        user = User.read_by_id(id_)
        user.balance = randint(0, 1_000_000)
        result = User.update(user)
        self.assertNotEqual(result, False)
        new_user = User.read_by_id(id_)
        self.assertEqual(new_user.balance, user.balance)

    def test_update_user_without_id(self):
        """
        Тестирование обновления пользователя без идентификатора
        """
        user = User(code="4579",
                    card_number="1677",
                    payment_system="МастерМир",
                    balance=10_000)
        self.assertRaises(ValueError, User.update, user)

    def test_delete_user(self):
        """
        Тестирование удаления пользователя
        """
        id_ = 1
        result = User.delete(id_)
        self.assertEqual(result, True)
        user = User(id=1,
                    code="4579",
                    card_number="1677",
                    payment_system="МастерМир",
                    balance=10_000)
        User.create(user)
