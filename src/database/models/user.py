"""
Описание модели пользователя
"""

__author__ = "Kirill Petryashev"

from typing import Type
from sqlalchemy import Column, Integer, Text, CheckConstraint
from sqlalchemy.orm import Session
from ..utilities.database import Base, ENGINE


class User(Base):
    """
    Описание пользователя

    id - Целочисленный идентификатор пользователя
    code - Пин-код пользователя для банкомата
    card_number - Последние четыре цифры карты пользователя
    payment_system - Платёжная система
    balance - Количество денег на счёте пользователя
    """
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    code = Column("code", Text, CheckConstraint("code ~ '^[0-9]{4}$'::text"), nullable=False,
                  unique=True)
    card_number = Column("card_number", Text, CheckConstraint("card_number ~ '^[0-9]{4}$'::text"),
                         nullable=False)
    payment_system = Column("payment_system", Text, nullable=False)
    balance = Column("balance", Integer, CheckConstraint("balance::numeric::integer > 0"), default=0)

    @classmethod
    def update_user_balance(cls, id_: int, new_balance: int) -> None:
        """
        Обновление баланса пользователя

        :param id_: Идентификатор пользователя
        :type id_: int
        :param new_balance: Новое значение баланса пользователя
        :type new_balance: int
        """
        if new_balance < 0:
            raise Exception("Баланс не может быть отрицательным!")
        with Session(autoflush=False, bind=ENGINE) as db:
            user = db.get(User, id_)
            if user is None:
                raise Exception("Такого пользователя не существует")
            user.balance = new_balance
            db.commit()


def add_user(user: User) -> None:
    """
    Добавление пользователя в базу данных

    :param user: Пользователь для добавления
    :type user: User
    """
    with Session(autoflush=False, bind=ENGINE) as db:
        db.add(user)
        db.commit()


def read_user(id_: int) -> Type[User]:
    """
    Чтение пользователя из базы данных

    :param id_: Идентификатор пользователя в базе
    :type id_: int
    :returns: Пользователь или ничего, в случае если
              пользователь не будет найден.
    :rtype: User | None
    """
    with Session(autoflush=False, bind=ENGINE) as db:
        user = db.get(User, id_)
        if user is not None:
            return user
