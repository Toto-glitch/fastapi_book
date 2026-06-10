from .base import BaseRepository
from models import Author


class AuthorRepository(BaseRepository):
    model = Author
