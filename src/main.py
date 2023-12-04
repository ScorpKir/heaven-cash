"""
Точка входа приложения
"""

__author__ = "Kirill Petryashev"

from fastapi import FastAPI
from src.api import user

app = FastAPI(title="heaven-cash")

# Подключаем роутеры
app.include_router(user.router, prefix="/api")
