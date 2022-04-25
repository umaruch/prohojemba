import uvicorn
from fastapi import FastAPI

from src.core.builder import ApplicationBuilder


def create_application() -> FastAPI:
    """
        Создание экземпляра приложения    
    """
    pass


app = create_application()
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

