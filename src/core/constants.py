from enum import Enum


class TitleTypes(Enum):
    GAME = "games"
    MOVIE = "movies"
    SERIES = "series"
    ANIME = "animes"
    BOOK = "books"
    COMIC = "comics"
    MANGA = "mangas"


class ActivityStates(Enum):
    PLANNED = "planned"
    ACTIVE = "active"
    COMPLETE = "completed"
