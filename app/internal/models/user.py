"""
Описание модели пользователя
"""

__author__ = "Kirill Petryashev, Dmitry Leminchuk"

from typing import Optional
from pydantic import BaseModel, ConfigDict, constr, conint, confloat

from app.package.database.models.user import UserDatabaseModel


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
    balance: confloat(ge=0.00)

    def to_database_model(self) -> UserDatabaseModel:
        """
        Конвертация модели пользователя
        в модель для базы данных

        :returns: Модель пользователя для базы данных
        :rtype: UserDatabaseModel
        """
        return UserDatabaseModel(**self.model_dump())

    @classmethod
    def create(cls, user) -> int:
        """
        Добавление пользователя

        :param user: Пользователь для создания
        :type user: User

        :returns: Идентификатор только что созданного пользователя
        :rtype: int
        """
        id_ = UserDatabaseModel.create(user.to_database_model())
        return id_

    @classmethod
    def read_by_id(cls, id_: int):
        """
        Чтение пользователя по идентификатору

        :param id_: Идентификатор пользователя
        :type id_: int

        :returns: Пользователь или ничего, в случае если
                  пользователь не будет найден.
        :rtype: User | None
        """
        db_user = UserDatabaseModel.read_by_id(id_)
        if db_user:
            return cls.model_validate(db_user.to_dict())

    @classmethod
    def read_by_code(cls, code: str):
        """
        Чтение пользователя по пин-коду карты

        :param code: Пин-код пользователя
        :type code: str

        :returns: Пользователь или ничего, в случае если
                  пользователь не будет найден.
        :rtype: User | None
        """
        if not code.isdigit() or not len(code) == 4:
            raise ValueError("Неверный формат пин-кода")
        db_user = UserDatabaseModel.read_by_code(code)
        if db_user:
            return cls.model_validate(db_user.to_dict())

    @classmethod
    def read_id_by_code(cls, code: str):
        """
        Чтение идентификатора пользователя по пин-коду карты

        :param code: Пин-код пользователя
        :type code: str

        :returns: Пользователь или ничего, в случае если
                  пользователь не будет найден.
        :rtype: User | None
        """
        user = cls.read_by_code(code)
        if user:
            return user.id

    @classmethod
    def update(cls, user):
        """
        Обновление пользователя

        :param user: Пользователь с новыми данными
        :type user: User

        :param user: Пользователь для обновления
        :type user: User
        """
        if not user.id:
            raise ValueError("Отсутствует идентификатор пользователя")
        return UserDatabaseModel.update(user.to_database_model())

    @classmethod
    def delete(cls, id_: int) -> bool:
        """
        Удаление пользователя

        :param id_: Идентификатор пользователя для удаления
        :type id_: int

        :returns: Логическое значение обозначающее успех операции
        :rtype bool:
        """
        return UserDatabaseModel.delete(id_)
