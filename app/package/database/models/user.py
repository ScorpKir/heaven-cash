"""
Модель пользователя для базы данных
"""

__author__ = "Kirill Petryashev"

from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, Text, text

from app.package.database.database import Base, ENGINE


class UserDatabaseModel(Base):
    """
    Модель пользователя для базы данных
    """
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    code = Column("code", Text, nullable=False, unique=True)
    card_number = Column("card_number", Text, nullable=False)
    payment_system = Column("payment_system", Text, nullable=False)
    balance = Column("balance", Integer, default=0)

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

    @classmethod
    def create(cls, user) -> int:
        """
        Добавление пользователя в базу данных

        :param user: Пользователь для создания
        :type user: UserDatabaseModel

        :returns: Идентификатор только что созданного пользователя
        :rtype: int
        """
        with Session(autoflush=False, bind=ENGINE) as db:
            db.add(user)
            db.commit()
            db.refresh(user)
            return user.id

    @classmethod
    def read_by_id(cls, id_: int):
        """
        Чтение пользователя из базы данных по идентификатору

        :param id_: Идентификатор пользователя
        :type id_: int

        :returns: Пользователь или ничего, в случае если
                  пользователь не будет найден.
        :rtype: UserDatabaseModel | None
        """
        with Session(autoflush=False, bind=ENGINE) as db:
            return db.get(cls, id_)

    @classmethod
    def read_by_code(cls, code: str):
        """
        Чтение пользователя из базы данных по пин-коду карты

        :param code: Пин-код пользователя
        :type code: str

        :returns: Пользователь или ничего, в случае если
                  пользователь не будет найден.
        :rtype: UserDatabaseModel | None
        """
        with Session(autoflush=False, bind=ENGINE) as db:
            statement = text(f"users.code = '{code}'")
            db_user = db.query(cls).filter(statement).first()
            return db_user

    @classmethod
    def update(cls, user) -> bool:
        """
        Обновление пользователя в базе данных

        :param user: Пользователь с новыми данными
        :type user: UserDatabaseModel

        :returns: Логическое значение обозначающее успех операции
        :rtype: bool
        """
        with Session(autoflush=False, bind=ENGINE) as db:
            user_db = db.get(cls, user.id)
            if user_db:
                user_db.balance = user.balance
                db.commit()
                db.refresh(user_db)
                return True
            return False

    @classmethod
    def delete(cls, id_: int) -> bool:
        """
        Удаление пользователя из базы данных

        :param id_: Идентификатор пользователя для удаления
        :type id_: int

        :returns: Логическое значение обозначающее успех операции
        :rtype: bool
        """
        with Session(autoflush=False, bind=ENGINE) as db:
            db_user = db.get(cls, id_)
            if db_user:
                db.delete(db_user)
                db.commit()
                return True
            return False
