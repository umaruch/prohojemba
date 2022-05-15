from re import L
import typing
from typing import TypeVar, Optional, List
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession


Model = TypeVar("Model")


class BaseCRUD:
    def __init__(self) -> None:
        pass

    def _select_one(cls, db: AsyncSession) -> Optional[Model]:
        pass

    def _select_all(cls, db: AsyncSession) -> Optional[List[Model]]:
        pass

    def _exists(cls, db: AsyncSession) -> bool:
        pass

    def _create(cls, db: AsyncSession) -> Model:
        pass

    def _update(cls, db: AsyncSession) -> None:
        pass

    def _delete(cls, db: AsyncSession) -> None:
        pass