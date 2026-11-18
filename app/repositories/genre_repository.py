from models import Genre

from .base import BaseRepository


class GenreRepository(BaseRepository[Genre]):
    model = Genre
