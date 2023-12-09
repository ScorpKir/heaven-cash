"""
Запуск приложения
"""

__author__ = "Kirill Petryashev"

from fastapi import FastAPI
from app.configuration.server import Server


def create_app(_=None) -> FastAPI:
    """
    Создание приложения

    :returns: Проинициализированное приложение для запуска веб-сервером
    :rtype: FastAPI
    """
    app = FastAPI(title="heaven-cash")
    return Server(app).get_app()
