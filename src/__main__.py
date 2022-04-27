import uvicorn
from fastapi import FastAPI

from src.core.builder import get_application


app = get_application()
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

