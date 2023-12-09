"""
Модель операции для базы данных
"""

__author__ = "Kirill Petryashev"

from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, Text, Date, Numeric, ForeignKey

from app.package.database.database import Base, ENGINE


class OperationDatabaseModel(Base):
    """
    Модель операции для базы данных
    """
    __tablename__ = "operations"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    user = Column("user", Integer, ForeignKey("users.id"), nullable=False)
    type = Column("type", Text, nullable=False)
    date = Column("date", Date, nullable=False)
    amount = Column("amount", Numeric, nullable=True)
    additional = Column("additional", Text, nullable=True)

    def to_dict(self) -> dict:
        """
        Преобразование модели к словарю

        :returns: Словарь с необходимыми полями
        :rtype: dict
        """
        return {
            "id": self.id,
            "user": self.user,
            "type": self.type,
            "date": self.date,
            "amount": self.amount,
            "additional": self.additional
        }

    @classmethod
    def create(cls, operation) -> int:
        """
        Добавление операции в базу данных

        :param operation: Операция для создания
        :type operation: OperationDatabaseModel

        :returns: Идентификатор созданной операции
        :rtype: int
        """
        with Session(autoflush=False, bind=ENGINE) as db:
            db.add(operation)
            db.commit()
            db.refresh(operation)
            return operation.id

    @classmethod
    def read_by_id(cls, id_: int):
        """
        Чтение операции из базы данных по идентификатору

        :param id_: Идентификатор операции
        :type id_: int

        :returns: Операция или ничего, в случае если,
                  операция не будет найдена.
        :rtype: OperationDatabaseModel | None
        """
        with Session(autoflush=False, bind=ENGINE) as db:
            return db.get(cls, id_)

    @classmethod
    def delete(cls, id_: int) -> bool:
        """
        Удаление операции из базы данных

        :param id_: Идентификатор операции для удаления
        :type id_: int

        :returns: Логическое значение обозначающее успех операции
        :rtype: bool
        """
        with Session(autoflush=False, bind=ENGINE) as db:
            db_operation = db.get(cls, id_)
            if db_operation:
                db.delete(db_operation)
                db.commit()
                return True
            return False
