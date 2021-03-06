from enum import Enum


class TitleTypes(str, Enum):
    GAME = "games"
    MOVIE = "movies"
    SERIES = "series"
    ANIME = "animes"
    BOOK = "books"
    COMIC = "comics"
    MANGA = "mangas"


class ActivityStates(str, Enum):
    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETE = "completed"


class ValidationTypes(str, Enum):
    REGISTRATION = "signin"
    RESTORE_PASSWORD = "restore_password"
    CHANGE_EMAIL = "change_email"
