"""
Точка входа приложения
"""

__author__ = "Kirill Petryashev"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api import user
from src.models.utilities.config import get_allowed_origins

app = FastAPI(title="heaven-cash")

# Разрешенные источники
origins = get_allowed_origins()

# Подключение разрешенных источников
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'])

# Подключаем роутеры
app.include_router(user.router, prefix="/api")
