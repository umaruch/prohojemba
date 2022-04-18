from fastapi import APIRouter

from server.api.endpoints import auth, users, titles, reviews, activities

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["Авторизация и аутентификация"])
api_router.include_router(users.router, prefix="/users", tags=["Пользователи"])
api_router.include_router(titles.router, prefix="/titles", tags=["Тайтлы"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["Обзоры"])
api_router.include_router(activities.router, prefix="/activities", tags=["Активности"])
