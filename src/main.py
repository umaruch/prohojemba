from fastapi import FastAPI, APIRouter


from src.core.config import get_app_settings
from src.core.events import create_start_app_handler, create_stop_app_handler
from src.api.base import routers 

def get_application() -> FastAPI:
    settings = get_app_settings()
    settings.configure_logging()

    application = FastAPI(**settings.fastapi_kwargs)

    application.add_event_handler(
        "startup", create_start_app_handler(app, settings)
    )
    application.add_event_handler(
        "shutdown", create_stop_app_handler(app)
    )

    main_router = APIRouter()
    for url, router in routers.items():
        main_router.include_router(router, prefix=url)
        
    application.include_router(main_router, prefix=settings.api_prefix)

    return application


app = get_application()