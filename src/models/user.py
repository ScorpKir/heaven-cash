"""
Описание модели пользователя
"""

__author__ = "Kirill Petryashev, Dmitry Leminchuk"

from typing import Optional
from sqlalchemy import Column, Integer, Text, CheckConstraint
from sqlalchemy.orm import Session
from pydantic import BaseModel, constr, conint, ConfigDict
from src.models.utilities.database import Base, ENGINE


class UserDatabaseModel(Base):
    """
    Модель пользователя для базы данных
    """
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    code = Column("code",
                  Text,
                  CheckConstraint("code ~ '^[0-9]{4}$'::text"),
                  nullable=False,
                  unique=True)
    card_number = Column("card_number",
                         Text,
                         CheckConstraint("card_number ~ '^[0-9]{4}$'::text"),
                         nullable=False)
    payment_system = Column("payment_system", Text, nullable=False)
    balance = Column("balance",
                     Integer,
                     CheckConstraint("balance::numeric::integer > 0"),
                     default=0)

    def to_dict(self) -> dict:
        """
        Преобразование модели к словарю

        :returns: Словарь с необходимыми полями
        :rtype: dict
        """
        return {
            "id": self.id,
            "code": self.code,
            "card_number": self.card_number,
            "payment_system": self.payment_system,
            "balance": self.balance
        }


class User(BaseModel):
    """
    Описание пользователя

    code - Пин-код пользователя для банкомата
    card_number - Последние четыре цифры карты пользователя
    payment_system - Платёжная система
    balance - Количество денег на счёте пользователя
    """

    model_config = ConfigDict(validate_assignment=True)

    id: Optional[conint(ge=1)] = None
    code: constr(pattern=r'^\d{4}$')
    card_number: constr(pattern=r'^\d{4}$')
    payment_system: str
    balance: conint(ge=0)

    def to_database_model(self) -> UserDatabaseModel:
        """
        Конвертация модели пользователя
        в модель для базы данных

        :returns: Модель пользователя для базы данных
        :rtype: UserDatabaseModel
        """
        return UserDatabaseModel(**self.model_dump())


def create_user(user: User) -> int:
    """
    Добавление пользователя в базу данных

    :param user: Пользователь для добавления
    :type user: User
    :returns: Идентификатор только что созданного пользователя
    :rtype: int
    """
    with Session(autoflush=False, bind=ENGINE) as db:
        db_user = user.to_database_model()
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user.id


def read_user(id_: int) -> Optional[User]:
    """
    Чтение пользователя из базы данных

    :param id_: Идентификатор пользователя в базе
    :type id_: int
    :returns: Пользователь или ничего, в случае если
              пользователь не будет найден.
    :rtype: UserDatabaseModel | None
    """
    with Session(autoflush=False, bind=ENGINE) as db:
        db_user = db.get(UserDatabaseModel, id_)
        if db_user is not None:
            return User.model_validate(db_user, from_attributes=True)


def update_user(user: User) -> Optional[User]:
    """
    Обновление пользователя в базе данных и
    получение обновленного пользователя в случае успеха

    :param user: Пользователь для обновления
    :type user: User
    :returns: Обновленный пользователь или ничего,
              если обновление не удалось
    :rtype: Optional[User]
    """
    with Session(autoflush=False, bind=ENGINE) as db:
        user_db = db.get(UserDatabaseModel, user.id)
        if user_db is not None:
            user_db.balance = user.balance
            db.commit()
            db.refresh(user_db)
            return User.model_validate(user_db, from_attributes=True)


def delete_user(id_: int) -> bool:
    """
    Удаление пользователя из базы данных

    :param id_: Идентификатор пользователя для удаления
    :type id_: int
    :returns: Логическое значение обозначающее успех операции
    :rtype bool:
    """
    with Session(autoflush=False, bind=ENGINE) as db:
        db_user = db.get(UserDatabaseModel, id_)
        if db_user is not None:
            db.delete(db_user)
            db.commit()
            return True
        return False
