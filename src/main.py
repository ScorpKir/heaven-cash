"""
Точка входа приложения
"""

__author__ = "Kirill Petryashev"

from fastapi import FastAPI
from src.api import user

app = FastAPI(title="heaven-cash")

# Подключаем роутеры
app.include_router(user.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn

    # Запускаем сервер с использованием uvicorn
    uvicorn.run(app, host="127.0.0.1", port=6969, reload=True)
