from fastapi import FastAPI


from src.core.config import get_app_settings
from src.core.events import create_start_app_handler, create_stop_app_handler


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

    return application


app = get_application()