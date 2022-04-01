from fastapi import FastAPI


from server.core.config import settings
from server.api.router import api_router


app = FastAPI()
app.include_router(api_router, prefix=settings.API_STR)