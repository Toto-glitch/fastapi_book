from .pagination import PaginationDep
from .repos import AuthorRepositoryDep, BookRepositoryDep, GenreRepositoryDep

__all__ = (
    "AuthorRepositoryDep",
    "BookRepositoryDep",
    "GenreRepositoryDep",
    "PaginationDep"
)
