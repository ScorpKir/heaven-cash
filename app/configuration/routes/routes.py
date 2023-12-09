"""
Регистрация маршрутов API
"""

__author__ = "Kirill Petryashev"

from dataclasses import dataclass
from fastapi import FastAPI


@dataclass(frozen=True)
class Routes:
    routers: tuple

    def register_routes(self, app: FastAPI) -> None:
        """
        Регистрация маршрутов в приложении

        :param app: Приложение, в котором необходимо зарегистрировать маршруты
        :type app: FastAPI
        """
        for router in self.routers:
            app.include_router(router, prefix="/api")
