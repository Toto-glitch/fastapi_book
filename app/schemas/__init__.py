from .author import AuthorCreate, AuthorResponse, AuthorUpdate
from .book import BookCreate, BookResponse, BookUpdate
from .genre import GenreCreate, GenreResponse, GenreUpdate
from .common import PaginationParams, ListResponse, DeleteResponse

BookResponse.model_rebuild()
__all__ = (
    "AuthorCreate",
    "AuthorResponse",
    "BookCreate",
    "BookResponse",
    "AuthorUpdate",
    "BookUpdate",
    "PaginationParams",
    "ListResponse",
    "DeleteResponse",
    "GenreCreate",
    "GenreResponse",
    "GenreUpdate",
)
