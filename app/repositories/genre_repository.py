from .base import BaseRepository
from models import Genre


class GenreRepository(BaseRepository[Genre]):
    model = Genre
