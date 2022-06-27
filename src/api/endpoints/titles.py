from typing import Optional
from fastapi import APIRouter, Form, UploadFile, File, Request


from src.core.constants import TitleTypes, ActivityStates
from src.schemes.titles import CreateTitleModel


router = APIRouter()


@router.get("", tags=["Тайтлы"])
async def get_titles(type: str, offset: int, limit: int) -> None:
    """
        Получение списка общей информации о тайтлах
    """


@router.post("", tags=["Тайтлы"])
async def create_title(
    name: str = Form(...),
    type: TitleTypes = Form(...),
    cover: Optional[UploadFile] = File(None),
    description: Optional[str] = Form(None),
    year: int = Form(...)
):
    """
        Создание новой записи о тайтле
    """
    title = CreateTitleModel(name=name, type=type, cover=cover, description=description, year=year)
    return title


@router.get("/{title_id}", tags=["Тайтлы"])
async def get_title(title_id: int, req: Request):
    """
        Получение полной информации о тайтле
    """
    print(req.headers["user-agent"])
    print(req.headers["sec-ch-ua-platform"])


@router.patch("/{title_id}", tags=["Тайтлы"])
async def change_title(title_id: int,
    name: Optional[str] = Form(None),
    type: Optional[str] = Form(None),
    cover: Optional[UploadFile] = File(None),
    description: Optional[str] = Form(None),
    year: Optional[int] = Form(None) 
):
    """
        Запрос на изменение информации о тайтле
    """
    pass


@router.delete("/{title_id}", tags=["Тайтлы"])
async def delete_title(title_id: int):
    """
        Удаление записи о тайтле
    """
    pass


@router.get("/{title_id}/activities", tags=["Активность"])
async def get_title_activities(title_id: int, limit: int, offset: int):
    """
        Получение списка пользовательских активностей, связанных с тайтлом
    """
    pass


@router.post("/{title_id}/activities", tags=["Активность"])
async def create_title_activity(title_id: int,
    state: ActivityStates = Form(...)
):
    pass
