from fastapi import FastAPI


from src.core.settings import Settings


class ApplicationBuilder:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._app = FastAPI()

    def _build_routers(self) -> None:
        pass

    def _build_exceptions(self) -> None:
        pass

    def _build_deps(self) -> None:
        pass

    def build(self) -> FastAPI:
        self._build_routers()
        self._build_exceptions()
        self._build_services()
        self._build_depends()
        return self._app