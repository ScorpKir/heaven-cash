"""
Инициализация приложения для веб-сервера
"""

__author__ = "Kirill Petryashev"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.configuration.routes import __routes__
from app.configuration.env_utils import get_allowed_origins


class Server:

    __app: FastAPI

    def __init__(self, app: FastAPI):
        self.__app = app
        self.__register_origins(app)
        self.__register_routes(app)

    def get_app(self) -> FastAPI:
        return self.__app

    @staticmethod
    def __register_origins(app):
        origins = get_allowed_origins()
        app.add_middleware(CORSMiddleware,
                           allow_origins=origins,
                           allow_credentials=True,
                           allow_methods=['*'],
                           allow_headers=['*'])

    @staticmethod
    def __register_routes(app):
        __routes__.register_routes(app)