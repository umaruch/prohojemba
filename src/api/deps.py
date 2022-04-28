from typing import Generator
from fastapi import Request


async def get_db_connection(req: Request) -> Generator:
    pass

def get_redis_connection():
    pass

def get_email_service():
    pass

def get_current_user_by_token():
    """
        Получение информации о пользователе из access токена
    """
    pass