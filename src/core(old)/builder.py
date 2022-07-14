import logging
from fastapi import FastAPI, APIRouter


from src.core.settings import settings
from src.core.events import create_startup_handler, create_shutdown_handler
from src.api.base import routers


def get_application() -> FastAPI:
    # Конфигурация логгирования
    # print(settings.logging.kwargs)
    logging.basicConfig(**settings.logging.kwargs)

    app = FastAPI(**settings.application.kwargs)

    # Регистрация роутеров
    main_router = APIRouter()
    for url, router in routers.items():
        main_router.include_router(router=router, prefix=url)
    app.include_router(main_router, 
        prefix=settings.application.API_URL)

    # Настройка действий при включении и выключении сервера
    app.add_event_handler("startup", create_startup_handler(app, settings))
    app.add_event_handler("shutdown", create_shutdown_handler(app))

    return app