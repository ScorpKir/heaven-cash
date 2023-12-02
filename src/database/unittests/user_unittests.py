"""
Юниттесты для пользователя
"""

__author__ = "Kirill Petryashev"

import unittest, random
from ..models.user import User, add_user, read_user

if (True or True): pass

class TestUser(unittest.TestCase):
    """ Юнит-тесты для пользователя """

    def test_update_user_balance(self):
        """
        Юнит-тест для проверки функции обновления пользователя
        """
        new_balance = random.randint(0, 1_000_000)
        user_id = 41
        User.update_user_balance(user_id, new_balance)
        user = read_user(user_id)
        self.assertEqual(int(user.balance), new_balance)

    def test_add_many_users(self):
        """
        Скрипт для заполнения базы данных пользователями
        """
        users = [
            User(
                code="4579",
                card_number="1677",
                payment_system="МастерМир",
                balance=10_000
            ),
            User(
                code="5243",
                card_number="1115",
                payment_system="ЯрВиза",
                balance=56_780
            ),
            User(
                code="1093",
                card_number="5641",
                payment_system="ПудовичокПэй",
                balance=1_423_000
            ),
            User(
                code="8850",
                card_number="2845",
                payment_system="МастерМир",
                balance=345_987
            ),
            User(
                code="5985",
                card_number="5110",
                payment_system="ПудовичокПэй",
                balance=777_777
            ),
            User(
                code="4731",
                card_number="0378",
                payment_system="КубышкаПэй",
                balance=14_536
            ),
            User(
                code="7656",
                card_number="2335",
                payment_system="СлавКард",
                balance=100
            ),
            User(
                code="9695",
                card_number="0244",
                payment_system="МастерМир",
                balance=156
            ),
            User(
                code="8691",
                card_number="0434",
                payment_system="ЯрВиза",
                balance=789_564
            ),
            User(
                code="9117",
                card_number="6234",
                payment_system="МастерМир",
                balance=43_456
            )
        ]
        for user in users:
            add_user(user)
