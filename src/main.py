"""
Точка входа приложения
"""

__author__ = "Kirill Petryashev"

from fastapi import FastAPI, Request
from fastapi.openapi.docs import get_swagger_ui_html
from src.api import user

app = FastAPI(title="heaven-cash")

# Подключаем роутеры
app.include_router(user.router, prefix="/api")


@app.get("/docs", include_in_schema=False)
async def get_documentation(request: Request):
    print(request.scope)
    print("хер")
    openapi_url = request.scope.get("root_path") + "/openapi.json"
    return get_swagger_ui_html(openapi_url=openapi_url, title="Swagger")


if __name__ == "__main__":
    import uvicorn

    # Запускаем сервер с использованием uvicorn
    uvicorn.run(app, host="127.0.0.1", port=6969, reload=True)
