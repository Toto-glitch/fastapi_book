from .author import AuthorCreate, AuthorResponse, AuthorUpdate
from .book import BookCreate, BookResponse, BookUpdate

BookResponse.model_rebuild()
__all__ = (
    "AuthorCreate",
    "AuthorResponse",
    "BookCreate",
    "BookResponse",
    "AuthorUpdate",
    "BookUpdate",
)
