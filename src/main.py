"""
Точка входа приложения
"""

__author__ = "Kirill Petryashev"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import user

app = FastAPI(title="heaven-cash")

# Разрешенные источники
origins = ["http://127.0.0.1",
           "http://127.0.0.1:8080",
           "https://127.0.0.1",
           "https://127.0.0.1:8080",
           "http://45.145.6.133",
           "http://45.145.6.133:8080",
           "https://45.145.6.133",
           "https://45.145.6.133:8080"]

# Подключение разрешенных источников
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'])

# Подключаем роутеры
app.include_router(user.router, prefix="/api")
