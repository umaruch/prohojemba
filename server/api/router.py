from fastapi import APIRouter

from server.api.endpoints import auth, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Авторизация и аутентификация"])
api_router.include_router(users.router, prefix="/users", tags="Пользователи")

