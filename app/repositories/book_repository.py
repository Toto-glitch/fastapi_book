from .base import BaseRepository
from models import Book


class BookRepository(BaseRepository[Book]):
    model = Book
