import logging
from typing import Dict, Any
from pydantic import SecretStr, PostgresDsn, RedisDsn

from src.core.settings.base import BaseAppSettings


class AppSettings(BaseAppSettings):
    debug: bool = False
    title: str = "Проходжемба"
    version: str = "0.0.3"

    docs_url: str = "/docs"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"

    api_prefix: str = "/api/v1"

    secret_key: SecretStr

    logging_file: str = "prohojemba.log" 
    logging_level: int = logging.INFO

    database_url: PostgresDsn
    database_max_connections: int = 10
    database_min_connections: int = 10
    
    redis_url: RedisDsn
    redis_max_connections: int = 10
    redis_min_connections: int = 10

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            "debug": self.debug,
            "title": self.title,
            "version": self.version,
            "docs_url": self.docs_url,
            "openapi_prefix": self.openapi_prefix,
            "openapi_url": self.openapi_url,
            "redoc_url": self.redoc_url
        }

    def configure_logging(self) -> None:
        logging.basicConfig(
            filename=self.logging_file,
            filemode="a",
            level=self.logging_level,
            format="%(asctime)s [%(levelname)s] %(message)s"
        )