from typing import Generator

from server.core.db import Session


def get_db_connection() -> Generator:
    """
        Создание сессии БД
    """
    try:
        conn = Session()
        yield conn
    finally:
        conn.close()


def get_redis_connection() -> Generator:
    """
        Создание соединения с redis
    """
    pass


def auth_by_token():
    """
        Получение id пользователя по access токену
    """
    pass


