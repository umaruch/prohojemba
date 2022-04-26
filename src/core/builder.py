import logging
from fastapi import FastAPI


from src.core.settings import Settings


class ApplicationBuilder:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._app = FastAPI()

    def _config_logging(self) -> None:
        """
            Глобальная настройка логгирования
        """
        logging.basicConfig(**self._settings.logging.to_kwargs())

    def _build_events(self) -> None:
        # TODO Здесь настроить подключение к базе данных при запуске приложения, и закрытие всех подключений при выключении
        pass

    def _build_routers(self) -> None:
        pass

    def _build_exceptions(self) -> None:
        pass

    def _build_deps(self) -> None:
        pass

    def build(self) -> FastAPI:
        self._config_logging()
        self._build_routers()
        self._build_exceptions()
        return self._app